export class Pagination {
    private _data_list: any[]
    private _page = 1
    private _page_size: number
    private _length = 0

    constructor(list: any[], size = 10) {
        this._data_list = list
        this._page_size = size
    }

    get data_list() {
        return this._data_list
    }

    set data_list(list: any[]) {
        this._data_list = list
        this._page = 1
    }

    get length() {
        return this._length
    }
    set length(length: number) {
        this._length = length
    }

    set page(page: number) {
        this._page = page
    }
    get page() {
        return this._page
    }

    set page_size(page: number) {
        this._page_size = page
    }
    get page_size() {
        return this._page_size
    }

    get_data(): any[] {
        return this._data_list.slice((this._page - 1) * this._page_size, this._page * this._page_size)
    }

    filter(obj: any) {
        const new_data_list = this._data_list.filter(ele => {
            let flag = true
            for (const key in obj) {
                const value = obj[key]
                if (ele[key] !== value) {
                    flag = false
                }
            }
            return flag
        })
        this._length = new_data_list.length
        return new_data_list.slice((this._page - 1) * this._page_size, this._page * this._page_size)
    }
}