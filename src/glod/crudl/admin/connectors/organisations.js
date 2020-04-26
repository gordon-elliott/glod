import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const organisations = createResourceConnector('organisations', `
    id, referenceNo, name, category, status
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const organisationOptions = createOptionsConnector('organisationOptions', 'id', 'name')

module.exports = {
    organisations,
    organisationOptions
}
