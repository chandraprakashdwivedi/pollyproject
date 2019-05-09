node('master'){
      checkout scm
      stage('Deploy using serverless framework'){
          def DeployCloudFormation = load "$JENKINS_HOME/jobs/${env.JOB_NAME}/workspace/ci/jenkins/script/deploy-stack.groovy"
          def RemoveCloudFormation = load "$JENKINS_HOME/jobs/${env.JOB_NAME}/workspace/ci/jenkins/script/delete-stack.groovy"
          DeployCloudFormation.Deploy()
          //RemoveCloudFormation.Delete() //to delete stack
      }
      stage('Data upload'){
          //  sh 'ansible-playbook data-upload.yml'
    }
}
