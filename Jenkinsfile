pipeline {
    agent none
    stages {
        stage ('SAST') {
            agent {
                docker {
                    label 'parham'
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
        stage('Build'){
            agent {
                label 'parham'
            }
            steps {
                sh 'docker build -t parham/myproject:latest .'
                echo '> package docker image into tar file ...'
                sh 'docker save parham/myproject:latest > parhamProject.tar'
                stash includes: '**/*.tar', name:'DockerImage'
            }
        }
        stage('Test'){
            agent {
                docker {
                    label 'master'
                    image 'python:3.7-alpine'
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'cd src && cp main.py app.py'
                sh 'cd src && python test.py'
            }
        }
        stage('CIST'){
            agent {
                label 'parham'
            }
            steps {
                sh  'export PHONITO_API_TOKEN="${PHONITO_API_TOKEN}"'
                sh 'phonito-scanner -i parham/myproject:latest || true'
            }
        }
        stage('DAST'){
            agent {
                label 'parham'
            }
            steps {
                unstash 'DockerImage'
                echo '> load previous image on docker  ...'
                sh 'docker load < parhamProject.tar'
                sh 'docker run -itd -p 5050:5050 --name SecTest parham/myproject:latest'
                sh 'docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:5050/ || true'
            }
            post {
                failure {
                    sh 'docker stop SecTest'
                }
            }
        }
        stage('Deploy'){
            agent {
                label 'parham'
            }
            when {
                expression {env.GIT_BRANCH == 'origin/master'}
            }
            input {
                message 'Continue to Deploy?'
            }
            steps {
                sh 'docker run -itd parham/myproject:latest'
            }            
        }
    }
}
