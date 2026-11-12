"""Build isolated generic and WorkBuddy skill ZIPs from the same body."""
from pathlib import Path
import zipfile
import yaml

root = Path(__file__).resolve().parent
source = root / 'skills/laowang-github-sidehustle'
dist = root / 'dist'
dist.mkdir(exist_ok=True)
skill = (source / 'SKILL.md').read_text()
_, meta, body = skill.split('---', 2)
generic = yaml.safe_load(meta)
market = {
    'name': generic['name'],
    'display_name': '老王 GitHub 副业雷达',
    'display_name_en': 'Laowang GitHub Side Hustle Radar',
    'description': generic['description'],
    'description_zh': '发现开源副业方向，拆解买家、最小改造、收费方式和需求验证。',
    'description_en': 'Find GitHub side hustle ideas with buyer hypotheses, minimal changes, monetization and validation.',
    'version': '0.1.0',
    'author': '中年老王学 ai',
    'examples_zh': ['帮我找适合个人 AI Coding 的副业项目', '哪些开源工具适合做可重复销售的小产品？'],
    'examples_en': ['Find GitHub projects suitable for a solo side hustle.',
                    'Which open-source tools could become repeatable digital products?']
}
for variant in ('generic', 'workbuddy'):
    target = dist / f'laowang-github-sidehustle-{variant}.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            data = path.read_bytes()
            if variant == 'workbuddy' and path.name == 'SKILL.md':
                data = ('---\n' + yaml.safe_dump(market, allow_unicode=True, sort_keys=False) + '---' + body).encode()
            archive.writestr('laowang-github-sidehustle/' + str(path.relative_to(source)), data)
        archive.write(root / 'LICENSE', 'laowang-github-sidehustle/LICENSE')
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        content = archive.read('laowang-github-sidehustle/SKILL.md').decode()
        parsed = yaml.safe_load(content.split('---', 2)[1])
        assert parsed['name'] == generic['name']
        if variant == 'workbuddy':
            assert all(parsed.get(k) for k in market)
            assert len(parsed['examples_zh']) == len(parsed['examples_en'])
    print(target)
