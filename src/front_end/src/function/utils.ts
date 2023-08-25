import { get_source_list } from "@/request/api"
import { IStateModel } from "@/type/start"

export function source_judge() {
    //获取源清单
    let whole_array: IStateModel[]
    get_source_list().then((res: any) => {
        whole_array = res.source.map((ele: any) => {
            return {
                label: ele,
                is_checked: true,
            }
        })
        return whole_array
    })
}