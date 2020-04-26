import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const parishioners = createResourceConnector('parishioners', `
    id, referenceNo, surname, firstName, title, spouse, address1, address2, address3, county, eircode, child1, dob1, child2, dob2, child3, dob3, child4, dob4, telephone, giving, email
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const parishionerOptions = createOptionsConnector('parishionerOptions', 'id', 'surname')

module.exports = {
    parishioners,
    parishionerOptions
}
