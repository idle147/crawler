

interface ISelectDate {
  current_page: number, // 当前页
  total_count: number, //总条数
  single_page_size: number, //默认一页显示几条

}

export interface IStateData {
  id: number,
  date: string,
  keywords: string,
  source: string,
  state: string
  // log: string, // 日志信息
}

export interface IDetailData {
  id: number,
  title: string,
  icon: string,
  content: string,
  source: string,
  is_piracy: boolean
}
export class SearchData {
  // 表单定义
  select_data: ISelectDate = {
    current_page: 1,
    total_count: 0,
    single_page_size: 5,
  }
  // 展示的内容数据
  list: IStateData[] = []
}

export class DetailData {
  // 表单定义
  select_data: ISelectDate = {
    current_page: 1,
    total_count: 0,
    single_page_size: 5,
  }
  // 展示的内容数据
  list: IDetailData[] = []
}

export interface IAbortRes {
  id: number,
  message: string
}

