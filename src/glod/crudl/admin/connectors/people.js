import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const people = createResourceConnector('people', `
    id, organisation{id, name}, familyName, givenName, status, title, mobile, email, dateOfBirth, dobIsEstimate
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const personOptions = createOptionsConnector('personOptions', 'id', 'familyName')

module.exports = {
    people,
    personOptions
}
