from fabric.contrib.files import exists, sed
from fabric.api import env, local, run
from fabric.operations import put

REPO_URL = 'git@github.com:Windsooon/Unicooo-django.git'


def deploy():
    site_folder = '/home/{0}/sites/{1}'.format(env.user, env.host)
    source_folder = site_folder + '/source'
    # create directory to store code and other
    _create_directory(site_folder)
    # get code from Github
    _get_latest_source(source_folder)
    _add_local_file(site_folder, source_folder)
    _update_compose(source_folder)
    _run_docker(source_folder)


def _create_directory(site_folder):
    run('mkdir -p {0}'.format(site_folder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd {0} && git reset --hard {1}'.format(
        source_folder, current_commit))


def _add_local_file(site_folder, source_folder):
    put('./www/.secret.json', source_folder + '/www/')
    put('./www/common/qiniuSettings.py', source_folder + '/www/common/')
    sed(
        source_folder + '/www/Dockerfile',
        'pip install -r requirements.txt ' +
        '-i https://mirrors.ustc.edu.cn/pypi/web/simple/',
        'pip install -r requirements.txt')


def _update_compose(source_folder):
    if env.host == 'stage.unicooo.com':
        sed(
            source_folder + '/docker-compose-pro.yml',
            'unicooo.settings.production',
            'unicooo.settings.stage',
            backup='')
        sed(
            source_folder + '/docker-compose-pro.yml',
            'nginx_pro',
            'nginx',
            backup='')


def _run_docker(source_folder):
    run(
        'cd {0} && docker-compose -f docker-compose-pro.yml up -d --build'.format(source_folder))
