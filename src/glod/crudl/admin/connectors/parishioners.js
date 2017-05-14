import { continuousPagination, listQuery, transformErrors } from '../utils'

var parishioners = {
    query: {
        read: listQuery({
            name: 'parishioners',
            fields: 'id, referenceNo, surname, firstName, title, spouse, address1, address2, address3, county, eircode, child1, dob1, child2, dob2, child3, dob3, child4, dob4, telephone, giving, email',
            args: { first: 50 },
            prepareFilters: object => {
                let args = Object.getOwnPropertyNames(object).map(name => {
                    if (['referenceNo'].includes(name)) {
                        return `${name}: ${object[name]}`
                    }
                    else {
                        return `${name}: "${object[name]}"`
                    }
                }).join(', ')
                return args ? `{${args}}` : ''
            }
        }),
        create: `mutation ($input: ParishionerCreateLeafInput!) {
            parishionerCreate(input: $input) {
                errors
                parishioner {id, referenceNo, surname, firstName, title, spouse, address1, address2, address3, county, eircode, child1, dob1, child2, dob2, child3, dob3, child4, dob4, telephone, giving, email}
            }
        }`,
    },
    pagination: continuousPagination,
    transform: {
        readResponseData: data => data.data.parishioners.edges.map(e => e.node),
        createResponseData: data => {
            if (data.data.parishionerCreate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.parishionerCreate.errors))
            }
            return data.data.parishionerCreate.parishioner
        },
    },
}

var parishioner = {
    query: {
        read: `{parishioner(id: "%id"){id, referenceNo, surname, firstName, title, spouse, address1, address2, address3, county, eircode, child1, dob1, child2, dob2, child3, dob3, child4, dob4, telephone, giving, email}}`,
        update: `mutation ($input: ParishionerUpdateLeafInput!) {
            parishionerUpdate(input: $input) {
                errors
                parishioner {id, referenceNo, purpose, status, name, institution, sortCode, parishionerNo, BIC, IBAN}
            }
        }`,
    },
    transform: {
        readResponseData: data => {
            if (!data.data.parishioner) {
                throw new crudl.NotFoundError('The requested parishioner was not found')
            }
            return data.data.parishioner
        },
        updateResponseData: data => {
            if (data.data.parishionerUpdate.errors) {
                throw new crudl.ValidationError(transformErrors(data.data.parishionerUpdate.errors))
            }
            return data.data.parishionerUpdate.parishioner
        },
    }
}

module.exports = {
    parishioners,
    parishioner
}
