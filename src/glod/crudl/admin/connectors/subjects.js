import { continuousPagination, listQuery, transformErrors } from '../utils'

var subjects = {
    query: {
        read: listQuery({
            name: 'subjects',
            fields: 'id, name, selectVestrySummary, easterVestrySummary',
            args: { first: 50 },
            prepareFilters: object => {
                let args = Object.getOwnPropertyNames(object).map(name => {
                    return `${name}: "${object[name]}"`
                }).join(', ')
                return args ? `{${args}}` : ''
            }
        }),
        create: `mutation ($input: SubjectCreateLeafInput!) {
            subjectCreate(input: $input) {
                errors
                subject {id, name, selectVestrySummary, easterVestrySummary}
            }
        }`,
    },
    pagination: continuousPagination,
    transform: {
        readResponseData: data => data.data.subjects.edges.map(e => e.node),
        createResponseData: data => {
            if (data.data.subjectCreate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.subjectCreate.errors))
            }
            return data.data.subjectCreate.subject
        },
    },
}

var subject = {
    query: {
        read: `{subject(id: "%id"){id, name, selectVestrySummary, easterVestrySummary}}`,
        update: `mutation ($input: SubjectUpdateLeafInput!) {
            subjectUpdate(input: $input) {
                errors
                subject {id, name, selectVestrySummary, easterVestrySummary}
            }
        }`,
    },
    transform: {
        readResponseData: data => {
            if (!data.data.subject) {
                throw new crudl.NotFoundError('The requested subject was not found')
            }
            return data.data.subject
        },
        updateResponseData: data => {
            if (data.data.subjectUpdate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.subjectUpdate.errors))
            }
            return data.data.subjectUpdate.subject
        },
    }
}

module.exports = {
    subjects,
    subject
}
