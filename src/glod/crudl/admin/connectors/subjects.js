import { DEFAULT_PAGE_LENGTH } from '../constants'
import { createResourceConnector, createOptionsConnector } from '../connectors'
import continuousPagination from '../connectors/middleware/continuousPagination'

const subjects = createResourceConnector('subjects', `
    id, name, selectVestrySummary, easterVestrySummary
`)
.use(continuousPagination(DEFAULT_PAGE_LENGTH))

const subjectOptions = createOptionsConnector('subjectOptions', 'id', 'name')

module.exports = {
    subjects,
    subjectOptions
}
