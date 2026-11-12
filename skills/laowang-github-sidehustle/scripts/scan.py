#!/usr/bin/env python3
"""Collect public GitHub evidence. Standard library only; never executes repo code."""
import argparse
import base64
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class APIError(Exception):
    def __init__(self, status):
        self.status = status
        super().__init__(f'GitHub HTTP {status}')


def get(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'laowang-sidehustle/0.1'}
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    try:
        with urlopen(Request('https://api.github.com' + path, headers=headers), timeout=25) as response:
            return json.load(response)
    except HTTPError as error:
        raise APIError(error.code) from None


def collect(queries, limit, out):
    now = datetime.now(timezone.utc)
    result = {'fetched_at': now.isoformat(), 'queries': queries, 'scope': 'GitHub repository search sampling',
              'per_query_limit': limit, 'searches': [], 'repositories': [], 'errors': []}
    repos = {}
    for query in queries:
        try:
            data = get('/search/repositories?' + urlencode({'q': query, 'sort': 'updated', 'per_page': limit}))
            result['searches'].append({'query': query, 'total_matches': data['total_count'],
                                      'incomplete_results': data.get('incomplete_results', False)})
            for repo in data['items']:
                repos[repo['full_name']] = repo
        except (APIError, URLError, TimeoutError) as error:
            result['errors'].append({'stage': 'search', 'query': query, 'error': type(error).__name__,
                                     'status': getattr(error, 'status', None)})
            if getattr(error, 'status', None) in (401, 403, 429):
                break
    blocked = False
    for name, repo in repos.items():
        item = {key: repo.get(key) for key in ('full_name', 'html_url', 'description', 'homepage', 'topics',
                'language', 'stargazers_count', 'forks_count', 'open_issues_count', 'size', 'license',
                'created_at', 'pushed_at', 'archived', 'default_branch')}
        item['readme_status'] = 'not_attempted_rate_limit' if blocked else 'pending'
        if not blocked:
            try:
                data = get('/repos/' + name + '/readme')
                text = base64.b64decode(data['content']).decode('utf-8', errors='replace')
                item.update(readme=text[:16000], readme_truncated=len(text) > 16000,
                            readme_url=data['html_url'], readme_sha=data['sha'], readme_status='ok')
            except (APIError, URLError, TimeoutError, KeyError, ValueError) as error:
                item['readme_status'] = 'failed'
                result['errors'].append({'stage': 'readme', 'repo': name, 'error': type(error).__name__,
                                         'status': getattr(error, 'status', None)})
                blocked = getattr(error, 'status', None) in (401, 403, 429)
        result['repositories'].append(item)
    result['candidate_count'] = len(repos)
    result['readme_ok_count'] = sum(r['readme_status'] == 'ok' for r in result['repositories'])
    out.mkdir(parents=True, exist_ok=True)
    # A separate timestamped run preserves previous evidence; no shared history is silently overwritten.
    path = out / ('scan-' + now.strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'file': str(path.resolve()), 'candidates': len(repos),
                      'readme_ok': result['readme_ok_count'], 'errors': len(result['errors'])}, ensure_ascii=False))
    return 0 if repos and not result['errors'] else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query', action='append', help='GitHub repository search query; repeatable')
    parser.add_argument('--limit', type=int, default=10, help='1-30 repositories per query')
    parser.add_argument('--out', type=Path, default=Path('sidehustle-run'))
    args = parser.parse_args()
    if not 1 <= args.limit <= 30:
        parser.error('--limit must be 1-30')
    since = (datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat()
    queries = args.query or [f'topic:{topic} stars:>=50 pushed:>={since} archived:false fork:false'
                             for topic in ('saas', 'productivity', 'ecommerce')]
    # Reject credential-like search input rather than transmitting it accidentally.
    if any(re.search(r'(gh[pousr]_|github_pat_)', q) for q in queries):
        parser.error('Do not put tokens in search queries; use environment variables')
    return collect(queries, args.limit, args.out)


if __name__ == '__main__':
    sys.exit(main())
