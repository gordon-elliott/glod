import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const addresses = createResourceConnector('addresses', `
    id, address1, address2, address3, county, countryISO, eircode, telephone
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const addressOptions = createOptionsConnector('addressOptions', 'id', 'address1')

module.exports = {
    addresses,
    addressOptions
}
