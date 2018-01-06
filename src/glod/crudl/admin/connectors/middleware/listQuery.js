
function buildArgs(object, topLevel=false) {
    let args = Object.getOwnPropertyNames(object).map(name => {
        let value = object[name];
        if (value === Object(value)) {
            return `${name}: ${buildArgs(value)}`
        } else {
            return `${name}: ${JSON.stringify(value)}`
        }
    }).join(', ')
    if (topLevel) {
        return args ? `(${args})` : ''
    } else {
        return args ? `{${args}}` : ''
    }
}

function buildOrderBy(req) {
    if (req.sorting && req.sorting.length > 0) {
        const field = req.sorting[0] // Graphene supports only one orderBy column
        let prefix = field.sorted === 'ascending' ? '' : '-'
        return { orderBy: prefix + field.sortKey }
    }
    return {}
}

function buildFilters(req) {
    if (req.filters && Object.keys(req.filters).length > 0) {
        return { filters: req.filters }
    }
    return {}
}

function buildQueryString(req, options) {
    if (Object.prototype.toString.call(options.fields) === '[object Array]') {
        options.fields = options.fields.join(', ')
    }

    let args = buildArgs(Object.assign({},
        options.args,
        req.page,
        buildFilters(req),
        buildOrderBy(req),
        req.args
    ), true);
    return `{
        ${options.name} ${args} {
            totalCount, filteredCount,
            pageInfo { hasNextPage, hasPreviousPage, startCursor, endCursor }
            edges { node { ${options.fields} }}
        }
    }`
}

/**
* Use it like this:
*   const users = createGraphQLConnector().use(listQuery('users', 'id, username, email'))
*   users.read() // resolves to [ {id: '1', username: 'joe', email: 'joe@xyz.com' }, {...}, ... ]
*
* The list query does not require any parameters. So you can overload a connector with another read query:
*   users.use(query('read', '{ user (id: "%id") {id, username, email} }'))
*
* then you can do: `users.read()` to obtain a list of all users and `users(1).read()` to get the detail
* info of user with the id '1'
*/
export default function listQuery(namePl, fields, args) {
    const NamePl = namePl.charAt(0).toUpperCase() + namePl.slice(1);
    // TODO externalise naming scheme
    const options = { name: namePl, fields, args }

    return function listQueryMiddleware(next) {
        return {
            read: function (req) {
                if (req.resolved) {
                    return next.read(req)
                }

                // Build the query
                req.data = { query: buildQueryString(req, options) }

                return next.read(req).then((res) => {
                    const { totalCount, filteredCount, pageInfo, edges } = res.data.data[options.name]
                    // Split pagination from data
                    res.pagination = { totalCount, filteredCount, pageInfo }
                    res.data = edges.map(item => item.node)
                    return res
                })
            }
        }
    }
}
