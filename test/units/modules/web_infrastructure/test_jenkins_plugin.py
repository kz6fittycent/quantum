from io import BytesIO

from quantum.modules.web_infrastructure.jenkins_plugin import JenkinsPlugin
from quantum.module_utils.common._collections_compat import Mapping


def pass_function(*args, **kwargs):
    pass


GITHUB_DATA = {"url": u'https://api.github.com/repos/quantum/quantum',
               "response": b"""
{
  "id": 3638964,
  "name": "quantum",
  "full_name": "quantum/quantum",
  "owner": {
    "login": "quantum",
    "id": 1507452,
    "avatar_url": "https://avatars2.githubusercontent.com/u/1507452?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/quantum",
    "html_url": "https://github.com/quantum",
    "followers_url": "https://api.github.com/users/quantum/followers",
    "following_url": "https://api.github.com/users/quantum/following{/other_user}",
    "gists_url": "https://api.github.com/users/quantum/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/quantum/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/quantum/subscriptions",
    "organizations_url": "https://api.github.com/users/quantum/orgs",
    "repos_url": "https://api.github.com/users/quantum/repos",
    "events_url": "https://api.github.com/users/quantum/events{/privacy}",
    "received_events_url": "https://api.github.com/users/quantum/received_events",
    "type": "Organization",
    "site_admin": false
  },
  "private": false,
  "html_url": "https://github.com/quantum/quantum",
  "description": "Quantum is a radically simple IT automation platform that makes your applications and systems easier to deploy.",
  "fork": false,
  "url": "https://api.github.com/repos/quantum/quantum",
  "forks_url": "https://api.github.com/repos/quantum/quantum/forks",
  "keys_url": "https://api.github.com/repos/quantum/quantum/keys{/key_id}",
  "collaborators_url": "https://api.github.com/repos/quantum/quantum/collaborators{/collaborator}",
  "teams_url": "https://api.github.com/repos/quantum/quantum/teams",
  "hooks_url": "https://api.github.com/repos/quantum/quantum/hooks",
  "issue_events_url": "https://api.github.com/repos/quantum/quantum/issues/events{/number}",
  "events_url": "https://api.github.com/repos/quantum/quantum/events",
  "assignees_url": "https://api.github.com/repos/quantum/quantum/assignees{/user}",
  "branches_url": "https://api.github.com/repos/quantum/quantum/branches{/branch}",
  "tags_url": "https://api.github.com/repos/quantum/quantum/tags",
  "blobs_url": "https://api.github.com/repos/quantum/quantum/git/blobs{/sha}",
  "git_tags_url": "https://api.github.com/repos/quantum/quantum/git/tags{/sha}",
  "git_refs_url": "https://api.github.com/repos/quantum/quantum/git/refs{/sha}",
  "trees_url": "https://api.github.com/repos/quantum/quantum/git/trees{/sha}",
  "statuses_url": "https://api.github.com/repos/quantum/quantum/statuses/{sha}",
  "languages_url": "https://api.github.com/repos/quantum/quantum/languages",
  "stargazers_url": "https://api.github.com/repos/quantum/quantum/stargazers",
  "contributors_url": "https://api.github.com/repos/quantum/quantum/contributors",
  "subscribers_url": "https://api.github.com/repos/quantum/quantum/subscribers",
  "subscription_url": "https://api.github.com/repos/quantum/quantum/subscription",
  "commits_url": "https://api.github.com/repos/quantum/quantum/commits{/sha}",
  "git_commits_url": "https://api.github.com/repos/quantum/quantum/git/commits{/sha}",
  "comments_url": "https://api.github.com/repos/quantum/quantum/comments{/number}",
  "issue_comment_url": "https://api.github.com/repos/quantum/quantum/issues/comments{/number}",
  "contents_url": "https://api.github.com/repos/quantum/quantum/contents/{+path}",
  "compare_url": "https://api.github.com/repos/quantum/quantum/compare/{base}...{head}",
  "merges_url": "https://api.github.com/repos/quantum/quantum/merges",
  "archive_url": "https://api.github.com/repos/quantum/quantum/{archive_format}{/ref}",
  "downloads_url": "https://api.github.com/repos/quantum/quantum/downloads",
  "issues_url": "https://api.github.com/repos/quantum/quantum/issues{/number}",
  "pulls_url": "https://api.github.com/repos/quantum/quantum/pulls{/number}",
  "milestones_url": "https://api.github.com/repos/quantum/quantum/milestones{/number}",
  "notifications_url": "https://api.github.com/repos/quantum/quantum/notifications{?since,all,participating}",
  "labels_url": "https://api.github.com/repos/quantum/quantum/labels{/name}",
  "releases_url": "https://api.github.com/repos/quantum/quantum/releases{/id}",
  "deployments_url": "https://api.github.com/repos/quantum/quantum/deployments",
  "created_at": "2012-03-06T14:58:02Z",
  "updated_at": "2017-09-19T18:10:54Z",
  "pushed_at": "2017-09-19T18:04:51Z",
  "git_url": "git://github.com/quantum/quantum.git",
  "ssh_url": "git@github.com:quantum/quantum.git",
  "clone_url": "https://github.com/quantum/quantum.git",
  "svn_url": "https://github.com/quantum/quantum",
  "homepage": "https://www.quantum.com/",
  "size": 91174,
  "stargazers_count": 25552,
  "watchers_count": 25552,
  "language": "Python",
  "has_issues": true,
  "has_projects": true,
  "has_downloads": true,
  "has_wiki": false,
  "has_pages": false,
  "forks_count": 8893,
  "mirror_url": null,
  "open_issues_count": 4283,
  "forks": 8893,
  "open_issues": 4283,
  "watchers": 25552,
  "default_branch": "devel",
  "organization": {
    "login": "quantum",
    "id": 1507452,
    "avatar_url": "https://avatars2.githubusercontent.com/u/1507452?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/quantum",
    "html_url": "https://github.com/quantum",
    "followers_url": "https://api.github.com/users/quantum/followers",
    "following_url": "https://api.github.com/users/quantum/following{/other_user}",
    "gists_url": "https://api.github.com/users/quantum/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/quantum/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/quantum/subscriptions",
    "organizations_url": "https://api.github.com/users/quantum/orgs",
    "repos_url": "https://api.github.com/users/quantum/repos",
    "events_url": "https://api.github.com/users/quantum/events{/privacy}",
    "received_events_url": "https://api.github.com/users/quantum/received_events",
    "type": "Organization",
    "site_admin": false
  },
  "network_count": 8893,
  "subscribers_count": 1733
}
"""
               }


def test__get_json_data(mocker):
    "test the json conversion of _get_url_data"

    timeout = 30
    params = {
        'url': GITHUB_DATA['url'],
        'timeout': timeout
    }
    module = mocker.Mock()
    module.params = params

    JenkinsPlugin._csrf_enabled = pass_function
    JenkinsPlugin._get_installed_plugins = pass_function
    JenkinsPlugin._get_url_data = mocker.Mock()
    JenkinsPlugin._get_url_data.return_value = BytesIO(GITHUB_DATA['response'])
    jenkins_plugin = JenkinsPlugin(module)

    json_data = jenkins_plugin._get_json_data(
        "{url}".format(url=GITHUB_DATA['url']),
        'CSRF')

    assert isinstance(json_data, Mapping)
