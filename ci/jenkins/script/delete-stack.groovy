def Delete() {
sh '''#!/bin/bash -xe
 sls remove -v
'''
}
return this;
