'''
test_phishing_vector.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from ..helper import PluginTest, PluginConfig


class TestPhishingVector(PluginTest):
    
    target_url = 'http://moth/w3af/audit/phishing_vector/'
    
    _run_configs = {
        'cfg': {
            'target': target_url,
            'plugins': {
                 'audit': (PluginConfig('phishingVector'),),
                 'discovery': (
                      PluginConfig(
                          'webSpider',
                          ('onlyForward', True, PluginConfig.BOOL)),
                  )
                 
                 }
            },
        }
    
    def test_found_redirect(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])

        vulns = self.kb.getData('phishingVector', 'phishingVector')
        
        self.assertEquals(3, len(vulns))
        self.assertEquals(all(['Phishing vector' == vuln.getName() for vuln in vulns ]) , True)

        # Verify the specifics about the vulnerabilities
        expected = [
            ('http_blacklist_phishing.php', 'section'),
            ('iframe_phishing.php', 'url'),
            ('frame_phishing.php', 'url'),
        ]

        found = [ (str(v.getURL()), v.getVar()) for v in vulns]
        expected = [ ((self.target_url + end), param) for (end, param) in expected ]
        
        self.assertEquals(
                set( found ),
                set( expected )
                )
