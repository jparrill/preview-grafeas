import datetime
import random
import swagger_client
import json
from swagger_client.rest import ApiException
from pprint import pprint

class Archive(object):

    def base_image(self):
        images = [ "adminer", "aerospike", "alpine", "amazonlinux", "arangodb", "backdrop", "bash", "bonita", "buildpack-deps", "busybox", "cassandra", "centos", "chronograf", "cirros", "clearlinux", "clojure", "composer", "consul", "convertigo", "couchbase", "couchdb", "crate", "crux", "debian", "docker", "drupal", "eclipse-mosquitto", "eggdrop", "elasticsearch", "elixir", "erlang", "euleros", "fedora", "flink", "fsharp", "gazebo", "gcc", "geonetwork", "ghost", "golang", "gradle", "groovy", "haproxy", "haskell", "haxe", "hello-seattle", "hello-world", "hola-mundo", "httpd", "hylang", "ibmjava", "influxdb", "irssi", "jenkins", "jetty", "joomla", "jruby", "julia", "kaazing-gateway", "kapacitor", "kibana", "known", "kong", "lightstreamer", "logstash", "mageia", "mariadb", "maven", "mediawiki", "memcached", "mongo", "mongo-express", "mono", "mysql", "nats", "nats-streaming", "neo4j", "neurodebian", "nextcloud", "nginx", "node", "notary", "nuxeo", "odoo", "openjdk", "opensuse", "oraclelinux", "orientdb", "owncloud", "percona", "perl", "photon", "php", "php-zendserver", "piwik", "plone", "postgres", "pypy", "python", "r-base", "rabbitmq", "rakudo-star", "rapidoid", "redis", "redmine", "registry", "rethinkdb", "rocket.chat", "ros", "ruby", "rust", "sentry", "silverpeas", "solr", "sonarqube", "sourcemage", "spiped", "storm", "swarm", "swift", "swipl", "telegraf", "thrift", "tomcat", "tomee", "traefik", "ubuntu", "vault", "websphere-liberty", "wordpress", "xwiki", "znc", "zookeeper" ]

        return random.choice(images)

    def times(self):
        now = datetime.datetime.now()
        return now.isoformat()


class NoteComposser(object):
    '''Class to make easier the composition of a Note against Grafeas server'''

    def __init__(self, project_id, note_id):
        self.project_id = project_id
        self.note_id = note_id
        self.kind = 'PACKAGE_VULNERABILITY'
        self.note_data = {}

    def constructor(self, kind):
        if kind is 'PACKAGE_VULNERABILITY':
            return self.create_vulnerability()

        else:
            print "Error on constructor"

    def create_vulnerability(self):
        data = {}
        arc = Archive()

        data['base_image'] = arc.base_image()
        data['create_time'] = arc.times()
        data['update_time'] = arc.times()
        data['expiration_time'] = ''
        data['kind'] = self.kind
        data['long_description'] = ''
        data['name'] = 'project/{}/notes/{}'.format(self.project_id, self.note_id)
        data['package'] = 'poppler'
        data['related_url'] = 'https://security-tracker.debian.org/tracker/CVE-2017-14976'
        data['short_description'] = self.project_id
        data['vulnerability_type'] = 'Security'

        return data


    def push_note(self, data):
        if not data:
            self.note_data = self.constructor(self.kind)

        graf = swagger_client.GrafeasApi()
        projects_id = self.project_id
        note_id = self.note_id

        try:
            resp = graf.create_note(projects_id, note_id=note_id, note=self.note_data)
            pprint(resp)
        except ApiException as e:
            print "Exception when calling GrafeasApi->create_note: %s\n" % e


    def get_note(self):
        graf = swagger_client.GrafeasApi()
        try:
            resp = graf.get_note(self.project_id, self.note_id)
            pprint(resp)
        except ApiException as e:
            print "Exception when calling GrafeasApi->get_note: %s\n" % e
        



# create an instance of the API class
project_id = 'test01' # str | Part of `parent`. This field contains the projectId for example: \"project/{project_id}
note_id = 'CVE-2017-14976' # str | The ID to use for this note. (optional)

nc = NoteComposser(project_id, note_id)
nc.push_note(json.load(open('samples/note_sample.json')))
#nc.get_note()

