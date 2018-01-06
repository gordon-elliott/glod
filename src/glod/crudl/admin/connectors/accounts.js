import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const accounts = createResourceConnector('accounts', `
    id, referenceNo, purpose, status, name, institution, sortCode, accountNo, BIC, IBAN
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const accountOptions = createOptionsConnector('accountOptions', 'id', 'name')
// use accountOptions to match ids with accountLeaf rather than accountNode

module.exports = {
    accounts,
    accountOptions
}
