pipeline {
    agent any

    triggers {
        cron('0 10 * * *')
    }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        VENV_DIR = '.jenkins-venv'
    }

    stages {
        stage('Prepare Python') {   
            steps {
                powershell '''
                    python --version
                    if (-not (Test-Path $env:VENV_DIR)) {
                        python -m venv $env:VENV_DIR
                    }
                    & ".\\$env:VENV_DIR\\Scripts\\python.exe" -m pip install --upgrade pip
                '''
            }
        }
        stage('Install dependencies') {
            steps {
                powershell '''
                    & ".\\$env:VENV_DIR\\Scripts\\python.exe" -m pip install -r requirements.txt
                    & ".\\$env:VENV_DIR\\Scripts\\python.exe" -m playwright install
                '''
            }
        }

        stage('Run tests') {
            steps {
                powershell '''
                    New-Item -ItemType Directory -Force -Path reports | Out-Null
                    $python = ".\\$env:VENV_DIR\\Scripts\\python.exe"
                    & $python -m pytest -v tests/analytical_plan/test_analytical_plan.py `
                    tests/analytic_dataset/test_analytic_dataset.py `
                    tests/home/test_home.py `
                    tests/project_specs/test_project_spec.py `
                    tests/main_model/test_main_model.py `
                    tests/workbook/test_workbook.py `
                    tests/e2e/test_full_project_flow.py `
                    --alluredir=reports/allure-results `
                    --junitxml=reports/junit.xml
                '''
            }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Pytest HTML Report'
            ])
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/allure-results']]
            ])
            archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/**/*', fingerprint: true
            
        }
    }
}
