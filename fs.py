import yaml
import argparse
import sys

class DockerVersion(object):
    """Manage DockerTag version numbers"""

    def __init__(self, dockertag):
        self.dockertag = dockertag
        self.major, self.minor, self.release = self._get_version_for_type()


    def _get_version_for_type(self):
        """returns the version numbers for each version type. Major, minor, release"""
        vnum = self.dockertag.split('.')
        vnum[0] = vnum[0].strip('v')
        return int(vnum[0]), int(vnum[1]), int(vnum[2])


    def increment(self, versiontype):
        if versiontype.lower() == 'major':
            self.major += 1
        elif versiontype.lower() == 'minor':
            self.minor += 1
        elif versiontype.lower() == 'release':
            self.release += 1
        else:
            raise Exception('Unknown version type. Must be Major, Minor, Release.')

        self.dockertag = 'v{0}.{1}.{2}'.format(self.major, self.minor, self.release)
        return self.dockertag


    def decrement(self, versiontype):
        if versiontype.lower() == 'major':
            self.major -= 1
        elif versiontype.lower() == 'minor':
            self.minor -= 1
        elif versiontype.lower() == 'release':
            self.release -= 1
        else:
            raise Exception('Unknown version type. Must be Major, Minor, Release.')

        self.dockertag = 'v{0}.{1}.{2}'.format(self.major, self.minor, self.release)
        return self.dockertag


def loadyaml(filename):
    """Returns a dictionary from a yaml file"""

    with open(filename, 'r') as f:
        data = yaml.load(f)
    return data

def writeyaml(data, filename):
    """writes yaml to a file"""

    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def cmdline():
    """Creates a command line interface for the script"""

    parser = argparse.ArgumentParser()
    parser.add_argument('imagename', action='store', help='Docker image name')
    parser.add_argument('action', action='store', help='Increment (I) or decrement (D) a version number')
    parser.add_argument('versiontype', action='store', help='Specify Major, Minor, or Release')
    return parser.parse_args()

def main(input_file, output_file):
    """takes an input file and an output file"""

    data = loadyaml(input_file)
    cmd = cmdline()

    """Get the docker image version from the given image name.
    Give the user feedback if the image name isn't found in the given yaml file"""
    try:
        dockertag = data[cmd.imagename]['image']['dockerTag']
    except KeyError:
        print "{0} is not a valid docker image name. Please specify a valid image name.".format(cmd.imagename)
        sys.exit()

    """Set the docker image version here"""
    dver = DockerVersion(dockertag)
    if cmd.action.lower() == 'i' or cmd.action.lower() == 'increment':
        dockertag = dver.increment(cmd.versiontype)
    elif cmd.action.lower() == 'd' or cmd.action.lower() == 'decrement':
        dockertag = dver.decrement(cmd.versiontype)
    else:
        raise Exception('Unknown action type. Must be increment (I) or decrement (D)')

    """Set the new version info within the dictionary"""
    data[cmd.imagename]['image']['dockerTag'] = dockertag

    """Write out a yaml file with the new version information"""
    writeyaml(data, output_file)

if __name__ == '__main__':
    main('example.yaml', 'results.yaml')