def Deploy() {
sh '''#!/bin/bash -xe
 sls deploy -v
'''
}
return this;
