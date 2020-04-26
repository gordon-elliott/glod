import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const statementItems = createResourceConnector('statementItems', `
    id, account{id, name, IBAN}, date, details, currency, debit, credit, balance
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const statementItemOptions = createOptionsConnector('statementItemOptions', 'id', 'date')

module.exports = {
    statementItems,
    statementItemOptions
}
