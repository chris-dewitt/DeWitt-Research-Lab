@description('Azure region for the optional DRL portability deployment.')
param location string = resourceGroup().location

@description('Prebuilt Atticus container image URI.')
param containerImage string

@description('Short environment label such as dev or stage.')
@allowed([
  'dev'
  'stage'
])
param environmentName string = 'dev'

var suffix = uniqueString(resourceGroup().id)
var workspaceName = 'drl-${environmentName}-logs-${suffix}'
var managedEnvironmentName = 'drl-${environmentName}-aca-${suffix}'
var appName = 'atticus-foundation-${environmentName}'

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: workspaceName
  location: location
  properties: {
    retentionInDays: 30
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource managedEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: managedEnvironmentName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logs.properties.customerId
        sharedKey: logs.listKeys().primarySharedKey
      }
    }
  }
}

resource atticus 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: managedEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: false
        targetPort: 8080
        transport: 'auto'
      }
    }
    template: {
      containers: [
        {
          name: 'atticus'
          image: containerImage
          env: [
            {
              name: 'ATTICUS_HOST'
              value: '0.0.0.0'
            }
            {
              name: 'PORT'
              value: '8080'
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/healthz'
                port: 8080
              }
              initialDelaySeconds: 5
              periodSeconds: 30
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 2
      }
    }
  }
}

output containerAppName string = atticus.name
output defaultDomain string = managedEnvironment.properties.defaultDomain
