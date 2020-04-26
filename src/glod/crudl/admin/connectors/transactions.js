import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

// TODO include counterparty
const transactions = createResourceConnector('transactions', `
    id, referenceNo, publicCode, year, month, day, paymentMethod, description, amount, subject{id, name}, incomeExpenditure, FY, fund{id, name}
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const transactionOptions = createOptionsConnector('transactionOptions', 'id', 'reference_no')

module.exports = {
    transactions,
    transactionOptions
}
