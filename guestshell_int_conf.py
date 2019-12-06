import sys
import cli

cli.configurep(['int lo 100', 'ip address 10.0.100.1 255.255.255.0'])
cli.executep('show ip int b')
