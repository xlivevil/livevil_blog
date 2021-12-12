from fabric import task
from invoke import Responder
from _credentials import github_username, github_password, certbot_email


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username))
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(
            github_username),
        response='{}\n'.format(github_password))
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'livevil_blog'

    # 检查并安装supervisor
    # if c.run("supervisorctl").failed:
    #     c.run("pip install -U supervisor")

    # # 配置supervisor
    # c.run("mkdir -p ~/etc/supervisor/conf.d")
    # c.run("mkdir -p ~/etc/supervisor/var/log")

    # with c.cd(supervisor_conf_path):
    #     c.run("echo_supervisord_conf > supervisord.conf")

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl stop {}'.format(
            supervisor_program_name)
        c.run(cmd)

    project_root_path = '~/apps/livevil_blog/'

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 进入 static/plugin 目录，拉取前端调用的的插件
    with c.cd(project_root_path + 'blog/static/plugin/'):
        cmd = 'git clone https://github.com/pandao/editor.md.git'
        c.run(cmd)

    # 进入项目根目录，构建docker-compose
    with c.cd(project_root_path):
        cmd = 'docker-compose -f production.yml build'
        c.run(cmd)

    # 进入项目根目录，启动docker-compose
    with c.cd(project_root_path):
        cmd = 'docker-compose -f production.yml up'
        # cmd = 'supervisord -c ~/etc/supervisord.conf'
        c.run(cmd)

    # 进入项目根目录，启动certbot(已不再使用，改用了服务器商提供的长期证书)
    # with c.cd(project_root_path):
    #     cmd = 'docker exec -it livevil_blog_nginx certbot --nginx -{} -A -y -2 -2'.format(
    #         certbot_email)
    #     c.run(cmd)
