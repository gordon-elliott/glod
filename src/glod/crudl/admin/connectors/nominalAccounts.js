import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const nominalAccounts = createResourceConnector('nominalAccounts', `
    id, code, description, SOFAHeading, category, subCategory
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const nominalAccountOptions = createOptionsConnector('nominalAccountOptions', 'id', 'code')

module.exports = {
    nominalAccounts,
    nominalAccountOptions
}
