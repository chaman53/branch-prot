def notifyBuild(String buildStatus = 'BUILDING',String responseThread) {
  // build status of null means successful
  buildStatus =  buildStatus ?: 'SUCCESSFUL'

  // Default values
  def colorName = 'RED'
  def colorCode = '#FF0000'
  def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
  def summary = "${subject} (${env.BUILD_URL})"
  def details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""

  // Override default values based on build status
  if (buildStatus == 'BUILDING') {
    color = 'YELLOW'
    colorCode = '#FFFF00'
  } else if (buildStatus == 'BUILDING ML-MultiArticle-Summarisation-Openai') {
    color = 'ORANGE'
    colorCode = '#FFA500'
  } else if (buildStatus == 'DEPLOYING ML-MultiArticle-Summarisation-Openai') {
    color = 'PURPLE'
    colorCode = '#800080'
  }  else if (buildStatus == 'SUCCESSFUL') {
    color = 'GREEN'
    colorCode = '#00FF00'
  } else if (buildStatus == 'APPROVE') {
        color = 'BLUE'
        colorCode = '#00FFFF'
        subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' is waiting for manual approval (Auto cancel in 5 minutes)"
        summary = "${subject}  ${env.BUILD_URL}/input/"
  } else {
    color = 'RED'
    colorCode = '#FF0000'
  }

   // Send notifications
  slackSend (channel: responseThread, replyBroadcast: true ,color: colorCode, message: summary)
}
 def slackChannel = "pharma-nlp-alerts"

 def slackResponse = slackSend(channel: slackChannel, message: "Started PNLP STAGE Deployment build", color: '#00FF00')


pipeline {
  agent any
    stages {
        stage('GitSCM Clone') {
            steps {
                script {
                    checkout([$class: 'GitSCM',
                    branches: [[name: '*/stage']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [], submoduleCfg: [],
                    userRemoteConfigs: [[credentialsId: 'pharmanlp-git', url: 'https://github.com/capestart/PharmaNLP-ML-MultiArticle-Summarisation-Openai.git']]
                    ])
                }
            }
        }

	stage('SonarQube Analysis') {
	    steps {
	        script {
	            notifyBuild("SonarQube Scanning", slackResponse.threadId)
	            withSonarQubeEnv(credentialsId: 'sonar-token') {
	                def scannerHome = tool 'sonarscanner'
	
	                // Run SonarQube analysis
	                sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=PharmaNLP-ML-MultiArticle-Summarisation-Openai"
	
	                // Add hyperlink in the echo statement
			    def sonarReportUrl = 'https://stagesonarqube.pharmanlp.com/dashboard?id=PharmaNLP-ML-MultiArticle-Summarisation-Openai'
               		 notifyBuild("\nThe code vulnerability scan has been completed through SonarQube. Please check the report <${sonarReportUrl}|here> and fix the gaps as soon as possible.", slackResponse.threadId)

	            }
	        }
	    }
	}

	
        stage('Build and Push'){
            steps {
                script {
                     notifyBuild("BUILDING ML-MultiArticle-Summarisation-Openai",slackResponse.threadId)
                     sh label: '', script: '''
                     aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 384818357873.dkr.ecr.us-west-1.amazonaws.com
                     docker build -t pnlp-stage-ml-multiarticle-summarisation-openai .
                     docker tag pnlp-stage-ml-multiarticle-summarisation-openai:latest 384818357873.dkr.ecr.us-west-1.amazonaws.com/pnlp-stage-ml-multiarticle-summarisation-openai:latest
                     docker push 384818357873.dkr.ecr.us-west-1.amazonaws.com/pnlp-stage-ml-multiarticle-summarisation-openai:latest
                     echo "Successfully Build the ML-MultiArticle-Summarisation-Openai!!!"
                    '''
                }
            }
        }

        stage('Python Dependency Check') {
            steps {
                script {
                    // Use 'safety' or 'bandit' to check Python dependencies for security vulnerabilities
                    sh 'pip install safety' // Install safety tool
                    sh 'safety check --full-report' // Run safety check
                }
            }
        }
     
	
        stage('Approve'){
                        steps{
                        script{
                             notifyBuild("APPROVE",slackResponse.threadId)
                             timeout(time:5, unit:'MINUTES') {
                           input message:'Approve deployment?', submitter: 'approver'
                   }
              }
            }
        }
         stage('Deployment'){
            steps {
                script {
                    notifyBuild("DEPLOYING ML-MultiArticle-Summarisation-Openai",slackResponse.threadId)
                    sh label: '', script: '''
                           aws eks --region us-west-1 update-kubeconfig --name pnlp-stage-eks
                           kubectl get po
                           kubectl apply -f stage-pharmanlp-multiarticle-summarisation-openai.yaml
                           kubectl apply -f pharmanlp-service-multiarticle-summarisation-openai.yaml
                           kubectl rollout restart deployment/pharmanlp-multiarticle-summarisation-openai
                     echo "ML-Multi Article Summarisation Openai successfully deployed!!!"
                    '''
                }
            }
        }
	stage ('Starting downstream job') {
  	   steps {
    		build job: 'pnlp-stage-workspace-caches'
  	  }
       }
    }
    post {
         success {
             slackSend (channel: "pharma-nlp-alerts", color: '#00FF00', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
         }
         failure {
             slackSend (channel: "pharma-nlp-alerts", color: '#FF0000', message: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
         }
     }
}
