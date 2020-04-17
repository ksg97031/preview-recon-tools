from requests import get
from bs4 import BeautifulSoup

def badget_md(category, target):
    badge_url = "https://badgen.net/github/{category}/{target}".format(category=category, target=target)
    return "[![{category}]({badge_url})]({badge_url})".format(category=category, badge_url=badge_url)

if __name__ == '__main__':
    md = '| Name | URL | Description | Preview | Popularity | Metadata |'
    md += '\n| ---------- | :---------- | :---------- | :-----------: | :---------: | :----------: |'
    preview_md = "\n"
    with open('list.txt') as f:
        lines = f.read().strip().split("\n")
        for line in lines:
            github_url, preview_video_url = line.split()

            r = get(github_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            s = soup.find('span', {'itemprop':'about'})
            desc = s.text.strip()
            name = github_url.split("/")[-1]

            categories = ('contributors', 'watchers', 'last-commit', 'open-issues', 'closed-issues')

            target = github_url.split('github.com/')[1]
            popul = badget_md('stars', target)
            badges = list(map(lambda x : badget_md(x, target), categories))
            preview_link = "[Watch](#{0})".format(name)
            preview_md += "## {name}  \n[![asciicast]({preview_video_url}.svg)]({preview_video_url})\n".format(name=name,preview_video_url=preview_video_url)
                
            md += '\n| **{name}** | [{github_url}]({github_url}) | {desc} | {preview_link} | {popul} | {badges} |'.format(desc=desc, github_url=github_url, name=name, preview_link=preview_link, popul=popul, badges=' '.join(badges)) 

    with open('README.md', 'w+') as f:
        f.write(md)
        f.write(preview_md)
