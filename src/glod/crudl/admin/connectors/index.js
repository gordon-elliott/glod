import pluralize from 'pluralize'

import { createFrontendConnector, createBackendConnector } from '@crudlio/crudl-connectors-base'
import { crudToHttp, url, transformData } from '@crudlio/crudl-connectors-base/lib/middleware'

import crudlErrors from './middleware/crudlErrors'
import listQuery from './middleware/listQuery'
import query from './middleware/query'

const baseURL = '/graphql/'

// Base connector
export function createGraphQLConnector() {
    return createFrontendConnector(createBackendConnector())
        .use(crudToHttp({ create: 'post', read: 'post', update: 'post', delete: 'post' }))
        .use(url(baseURL))
}

/**
* A resource connector. Use it like this:
* const users = createResourceConnector('users', '_id, username, email')
*
* users.read()                 // list
* users.create({...})          // create
* users(id).read()             // detail
* users(id).delete()           // delete
* users(id).update({...})      // update
*/
export function createResourceConnector(namePl, fields) {
    const nameSg = pluralize.singular(namePl)
    const NameSg = nameSg.charAt(0).toUpperCase() + nameSg.slice(1)

    //-- CREATE QUERY --
    const createQuery = `
    mutation ($input: ${NameSg}CreateLeafInput!) {
        ${nameSg}Create (input: $input) {
            errors
            ${nameSg} { ${fields} }
        }
    }
    `
    const createQueryData = `${nameSg}Create.${nameSg}`    // e.g. addUser.user
    const createQueryError = `${nameSg}Create.errors`      // e.g. addUser.errors

    //-- READ QUERY --
    const readQuery = `{ ${nameSg} (id: "%_id") {${fields}} }`
    const readQueryData = nameSg

    //-- UPDATE QUERY --
    const updateQuery = `
    mutation ($input: ${NameSg}UpdateLeafInput!) {
        ${nameSg}Update (input: $input) {
            errors
            ${nameSg} {${fields}}
        }
    }
    `
    const updateQueryData = `${nameSg}Update.${nameSg}`     // e.g. changeUser.user
    const updateQueryError = `${nameSg}Update.errors`       // e.g. changeUser.errors

    //-- DELETE QUERY --
    const deleteQuery = `mutation { delete${NameSg} (id: "%_id") { deleted } }`
    const deleteQueryData = 'deleted'

    return createGraphQLConnector()
        .use(listQuery(namePl, fields))
        .use(query('create', createQuery, createQueryData, createQueryError))
        .use(query('read', readQuery, readQueryData))
        .use(query('update', updateQuery, updateQueryData, updateQueryError))
        .use(query('delete', deleteQuery, deleteQueryData))
        // Transform errors
        .use(crudlErrors)
}

/**
* USAGE: const options = createOptionsConnector('sections', '_id', 'name')
* options.read() // Resolves to { options: [ { value: '...', label: '...' }, { value: '...', label: '...' }, ...] }
*/
export function createOptionsConnector(namePl, valueKey, labelKey) {
    return createGraphQLConnector()
        .use(listQuery(namePl, `value: ${valueKey}, label: ${labelKey}`))
        .use(transformData('read', data => ({ options: data })))
}

export const login = createFrontendConnector(createBackendConnector())
    .use(url('/rest-api/login/'))
    .use(crudToHttp())
    .use(require('./middleware/crudlErrors').default) // rest-api errors
    .use(transformData('create',
        data => ({
            requestHeaders: { "Authorization": `Token ${data.token}` },
            info: data,
        })
    ))
