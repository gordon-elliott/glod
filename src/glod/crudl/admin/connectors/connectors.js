import { accounts, account } from './accounts'
import { nominalAccounts, nominalAccount } from './nominalAccounts'

module.exports = {

    accounts: accounts,
    account: account,

    nominalAccounts: nominalAccounts,
    nominalAccount: nominalAccount,

    // AUTHENTICATION
    login: {
        url: '/rest-api/login/',
        mapping: { read: 'post', },
        transform: {
            readResponse: res => {
                if (res.status >= 400) {
                    const error = res.data
                    if (error !== null && typeof error === 'object') {
                        error._error = error.non_field_errors
                    }
                    throw new crudl.ValidationError(error)
                }
                return res
            },
            readResponseData: data => ({
                requestHeaders: { "Authorization": `Token ${data.token}` },
                info: data,
            })
        }
    }
}
