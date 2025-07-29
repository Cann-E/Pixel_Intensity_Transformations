pipeline {
    agent { docker { image 'pmantini/assignment-cosc6380:latest' } }
    
    environment {
        PATH = "env/bin/:$PATH"
    }
    stages {
        stage('build') {
            steps {
                sh 'python hw3.py  > output/empty'                       
            }
        }                
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.* ', onlyIfSuccessful: true
        }
    }
}
