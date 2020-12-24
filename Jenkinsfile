pipeline {
    agent none
    stages {
        stage ('SAST') {
            agent {
                docker {
                    label 'master'
                    image 'maven:3-alpine'
                }
            }
            steps {
                withSonarQubeEnv('sonar') {
                    sh 'mvn sonar:sonar'
                    sh 'cat target/sonar/report-task.txt'
                }
            }
        }
        stage('Build Project'){
            agent {
                label 'parham'
            }
            steps {
                sh 'cd src && docker build -t parham/myproject:latest .'
            }
        }
        stage('Run Unit Test on Project'){
            agent {
                docker {
                    label 'master'
                    image 'python:3.7-alpine'
                }
            }
            steps {
                sh 'cd src && cp main.py app.py'
                sh 'cd src && pip install -r requirements.txt'
                sh 'cd src && python test.py'
            }
        }
        stage('Docker image security Test '){
            agent {
                label 'parham'
            }
            steps {
                sh  'export PHONITO_API_TOKEN="${PHONITO_API_TOKEN}"'
                sh 'phonito-scanner -i parham/myproject:latest  --fail-level HIGH'
            }
        }
        stage('DAST'){
            agent {
                label 'master'
            }
            steps {
                sh 'cd src && python3 main.py &'
                sh 'docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:5050/'
            }
        }
        stage('Deploy Project'){
            agent {
                label 'parham'
            }
            when {
                expression {env.GIT_BRANCH == 'origin/master'}
            }
            steps {
                sh 'docker run -itd parham/myproject:latest'
            }            
        }
    }
}