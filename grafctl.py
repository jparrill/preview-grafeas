import datetime
import click
import random
import swagger_client
import json
from swagger_client.rest import ApiException
from pprint import pprint
import logging
import os
import click
from os.path import dirname
from os.path import realpath

class Archive(object):

    def base_image(self):
        images = [ "adminer", "aerospike", "alpine", "amazonlinux", "arangodb", "backdrop", "bash", "bonita", "buildpack-deps", "busybox", "cassandra", "centos", "chronograf", "cirros", "clearlinux", "clojure", "composer", "consul", "convertigo", "couchbase", "couchdb", "crate", "crux", "debian", "docker", "drupal", "eclipse-mosquitto", "eggdrop", "elasticsearch", "elixir", "erlang", "euleros", "fedora", "flink", "fsharp", "gazebo", "gcc", "geonetwork", "ghost", "golang", "gradle", "groovy", "haproxy", "haskell", "haxe", "hello-seattle", "hello-world", "hola-mundo", "httpd", "hylang", "ibmjava", "influxdb", "irssi", "jenkins", "jetty", "joomla", "jruby", "julia", "kaazing-gateway", "kapacitor", "kibana", "known", "kong", "lightstreamer", "logstash", "mageia", "mariadb", "maven", "mediawiki", "memcached", "mongo", "mongo-express", "mono", "mysql", "nats", "nats-streaming", "neo4j", "neurodebian", "nextcloud", "nginx", "node", "notary", "nuxeo", "odoo", "openjdk", "opensuse", "oraclelinux", "orientdb", "owncloud", "percona", "perl", "photon", "php", "php-zendserver", "piwik", "plone", "postgres", "pypy", "python", "r-base", "rabbitmq", "rakudo-star", "rapidoid", "redis", "redmine", "registry", "rethinkdb", "rocket.chat", "ros", "ruby", "rust", "sentry", "silverpeas", "solr", "sonarqube", "sourcemage", "spiped", "storm", "swarm", "swift", "swipl", "telegraf", "thrift", "tomcat", "tomee", "traefik", "ubuntu", "vault", "websphere-liberty", "wordpress", "xwiki", "znc", "zookeeper" ]

        return random.choice(images)

    def times(self):
        now = datetime.datetime.now()
        return now.isoformat()


class NoteComposser(object):
    '''Class to make easier the composition of a Note against Grafeas server'''

    def create_vulnerability(self, project, note):
        data = {}
        arc = Archive()

        data['name'] = 'projects/{}/notes/{}'.format(project, note)
        data['shortDescription'] = project
        data['longDescription'] = project
        data['vulnerabilityType'] = 'Security'
        #data['buildType'] = ''
        data['baseImage'] = arc.base_image()
        data['package'] = {}
        data['package']['distribution'] = ''
        data['package']['name'] = '' 
        #data['deployable'] = ''
        #data['discovery'] = ''
        data['attestationAuthority'] = {}
        data['attestationAuthority']['hint'] = {}
        data['attestationAuthority']['hint']['humanReadableName'] = arc.base_image()
        data['relatedUrl'] = 'https://security-tracker.debian.org/tracker/%s' % project
        data['expirationTime'] = arc.times()
        data['createTime'] = arc.times()
        data['updateTime'] = arc.times()
        #data['operationName'] = ''
        data['kind'] = 'PACKAGE_VULNERABILITY' 
        #data['relatedNoteNames'] = 'test' 

        return data

class Grafctl(object):
    '''Class to manage Grafeas resources from CLI'''

    def __init__(self, verbose=False):
        # default
        self.file_path = dirname(realpath(__file__))
        self.verbose = verbose
        self.logger()

        # Grafeas stuff
        self.note_data = {}

    def logger(self):
        '''
        Function to log all actions
        '''
        self.log_filename = 'grafctl.log'
        if self.verbose:
            print 'Start Logging'

        log_file = self.file_path + '/' + self.log_filename
        logging.getLogger('').handlers = []
        if not os.path.exists(log_file):
            open(log_file, 'a').close()
            logging.basicConfig(
                filename=log_file,
                format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s',
                level=logging.INFO
            )
        else:
            logging.basicConfig(
                filename=log_file,
                format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s',
                level=logging.INFO
            )
        logging.info('Grafctl started...')

    def push_note(self, project_id, note_id, data):
        self.note_data = data
        graf = swagger_client.GrafeasApi()
        
        try:
            resp = graf.create_note(project_id, note_id=note_id, note=self.note_data)
        except ApiException as e:
            print "Exception when calling GrafeasApi->create_note: %s\n" % e

        return resp

    def get_note(self, project_id, note_id):
        graf = swagger_client.GrafeasApi()
        try:
            resp = graf.get_note(project_id, note_id)
        except ApiException as e:
            print "Exception when calling GrafeasApi->get_note: %s\n" % e

        return resp

    def get_occurrence(self, project_id, occurrence_id):
        graf = swagger_client.GrafeasApi()
        try:
            resp = graf.get_occurrence(project_id, occurrence_id)
        except ApiException as e:
            print "Exception when calling GrafeasApi->get_occurrence: %s\n" % e

        return resp

    def list_notes(self, project_id):
        graf = swagger_client.GrafeasApi()
        try:
            resp = graf.list_notes(project_id)
        except ApiException as e:
            print "Exception when calling GrafeasApi->list_notes: %s\n" % e

        return resp

    def list_note_occurrences(self, project_id, note_id):
        graf = swagger_client.GrafeasApi()
        try:
            resp = graf.list_note_occurrences(project_id, note_id)
        except ApiException as e:
            print "Exception when calling GrafeasApi->list_note_occurrences: %s\n" % e

        return resp

        
@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Debug mode')
@click.pass_context
def cli(ctx, verbose):
    ctx.obj['verbose'] = ctx.params['verbose']  

@click.command()
@click.option('-n', '--note', nargs=1, help='Note name to be pushed to Grafeas')
@click.option('-p', '--project', nargs=1, help='Project to store the related resource')
@click.option('-d', '--data', help='Note data to be uploaded into Grafeas project')
@click.pass_context
def push_note(ctx, note, project, data):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo()

    grafctl = Grafctl(ctx.obj['verbose'])

    if data == None:
        logging.info("Using constructor (mock), because not provided data")
        print "Using constructor (mock), because not provided data"
        nc = NoteComposser()
        note_data = nc.create_vulnerability(project, note)
    else:
        note_data = data

    if ctx.obj['verbose']:
        click.echo('Project: %s' % project)
        click.echo('Note: %s' % note)
        click.echo('Data:')
        click.echo(note_data)

    # Logging
    logging.info('----> Grafctl Start push event ')
    logging.info('Project: %s' % project)
    logging.info('Note: %s' % note)
    logging.info('Data:')
    logging.info(note_data)
    logging.info('----> Grafctl Finish push event ')
    logging.info('')

    # Push
    grafctl.push_note(project, note, note_data)

@click.command()
@click.option('-n', '--note', nargs=1, help='Note name to be fetch from Grafeas')
@click.option('-p', '--project', nargs=1, help='Project to get the related resource')
@click.pass_context
def get_note(ctx, note, project):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo()

    grafctl = Grafctl(ctx.obj['verbose'])


    # Logging
    logging.info('----> Grafctl Start get event ')
    logging.info('Project: %s' % project)
    logging.info('Note: %s' % note)
    logging.info('Action: Get')

    # Get
    note_data = grafctl.get_note(project, note)

    if ctx.obj['verbose']:
        click.echo('Project: %s' % project)
        click.echo('Note: %s' % note)
        click.echo('Action: Get Note')
        click.echo(note_data)

    logging.info(note_data)
    logging.info('----> Grafctl Finish get event ')
    logging.info('')


@click.command()
@click.option('-p', '--project', nargs=1, help='Project to get the related resource')
@click.pass_context
def list_notes(ctx, project):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo()

    grafctl = Grafctl(ctx.obj['verbose'])


    # Logging
    logging.info('----> Grafctl Start List event ')
    logging.info('Project: %s' % project)
    logging.info('Action: List Notes')

    # Get
    note_data = grafctl.list_notes(project)

    if ctx.obj['verbose']:
        click.echo('Project: %s' % project)
        click.echo('Action: List Notes')
        click.echo(note_data)

    logging.info(note_data)
    logging.info('----> Grafctl Finish List event ')
    logging.info('')

@click.command()
@click.option('-o', '--occurrence', nargs=1, help='Occurrence name to be fetch from Grafeas')
@click.option('-p', '--project', nargs=1, help='Project to get the related resource')
@click.pass_context
def get_occurrence(ctx, occurrence, project):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo()

    grafctl = Grafctl(ctx.obj['verbose'])

    # Logging
    logging.info('----> Grafctl Start Get event ')
    logging.info('Project: %s' % project)
    logging.info('Ocurrence: %s' % occurrence)
    logging.info('Action: List Ocurrences')

    # Get
    note_data = grafctl.get_occurrence(project, occurrence)

    if ctx.obj['verbose']:
        click.echo('Project: %s' % project)
        click.echo('Ocurrence: %s' % occurrence)
        click.echo('Action: Get Occurrence')
        click.echo(note_data)

    logging.info(note_data)
    logging.info('----> Grafctl Finish Get event ')
    logging.info('')

@click.command()
@click.option('-n', '--note', nargs=1, help='Note name to be fetch from Grafeas')
@click.option('-p', '--project', nargs=1, help='Project to get the related resource')
@click.pass_context
def list_occurrences(ctx, note, project):
    if ctx.obj['verbose']:
        click.echo('Verbose mode is %s' % (ctx.obj['verbose'] and 'on' or 'off'))
        click.echo()

    grafctl = Grafctl(ctx.obj['verbose'])

    # Logging
    logging.info('----> Grafctl Start List event ')
    logging.info('Project: %s' % project)
    logging.info('Note: %s' % note)
    logging.info('Action: List Ocurrences')

    # Get
    note_data = grafctl.list_note_occurrences(project, note)

    if ctx.obj['verbose']:
        click.echo('Project: %s' % project)
        click.echo('Note: %s' % note)
        click.echo('Action: List Notes')
        click.echo(note_data)

    logging.info(note_data)
    logging.info('----> Grafctl Finish List event ')
    logging.info('')

if __name__ == '__main__':
    cli.add_command(push_note)
    cli.add_command(get_note)
    cli.add_command(list_notes)
#    cli.add_command(push_ocurrence)
    cli.add_command(list_occurrences)
    cli.add_command(get_occurrence)
#    cli.add_command(delete_ocurrence)
#    cli.add_command(delete_note)
    cli(obj={})


### Samples
# python grafctl.py -v push_note -n 'note_02' -p 'myproject'
# python grafctl.py -v get_note -n 'note_02' -p 'myproject'
# python grafctl.py -v get_occurrence -o 'occurence_02' -p 'myproject'
# python grafctl.py -v list_notes -p 'myproject'
# python grafctl.py -v list_occurrences -p 'myproject' -n 'note_02'
###
