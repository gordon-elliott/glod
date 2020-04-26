import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const funds = createResourceConnector('funds', `
    id, name, restriction, isParishFund, account{id, name, IBAN}
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const fundOptions = createOptionsConnector('fundOptions', 'id', 'name')

module.exports = {
    funds,
    fundOptions
}
