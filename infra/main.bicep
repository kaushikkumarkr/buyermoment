targetScope = 'resourceGroup'

@description('Azure region for the dedicated BuyerMoment development footprint.')
param location string = resourceGroup().location
@description('Stable suffix used for globally unique Azure names.')
param nameSuffix string
@description('Environment label used for cost attribution.')
param environment string = 'dev'

var tags = {
  product: 'BuyerMoment'
  environment: environment
  costOwner: 'BuyerMoment'
  managedBy: 'buyerMoment-iac'
  creditGuardrail: 'startup-credit'
}
var storageName = 'stbuyermoment${nameSuffix}'
var registryName = 'acrbuymoment${nameSuffix}'
var keyVaultName = 'kv-buyermoment-${nameSuffix}'
var foundryName = 'buyermoment-foundry-${nameSuffix}'
var logsName = 'law-buyermoment-${nameSuffix}'
var containerEnvName = 'cae-buyermoment-${environment}'

resource logs 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logsName
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    features: { enableLogAccessUsingOnlyResourcePermissions: true }
    sku: { name: 'PerGB2018' }
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  tags: tags
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: registryName
  location: location
  tags: tags
  sku: { name: 'Basic' }
  properties: { adminUserEnabled: false }
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: 'Enabled'
    sku: { family: 'A', name: 'standard' }
  }
}

resource foundry 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: foundryName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  tags: tags
  properties: {
    customSubDomainName: foundryName
    publicNetworkAccess: 'Enabled'
  }
}

resource containerEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerEnvName
  location: location
  tags: tags
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

output storageAccountName string = storage.name
output storageBlobEndpoint string = storage.properties.primaryEndpoints.blob
output registryName string = registry.name
output registryLoginServer string = registry.properties.loginServer
output keyVaultName string = keyVault.name
output foundryName string = foundry.name
output foundryEndpoint string = foundry.properties.endpoint
output containerAppsEnvironmentName string = containerEnv.name

