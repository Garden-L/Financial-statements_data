import pandas as pd

class jamu:
    def __init__(self):
        self.df_list = [\
            pd.read_csv('20201분기손익.txt', sep='\t', encoding='cp949'),\
            pd.read_csv('20201분기손익연결.txt', sep='\t', encoding='cp949'),\
            pd.read_csv('20201분기포괄.txt', sep='\t', encoding='cp949'),\
            pd.read_csv('20201분기포괄연결.txt', sep='\t', encoding='cp949')]

        #실행
        self.modify_first()


    #항목조정
    def modify_first(self):
        self.mergeJamu = pd.DataFrame()
        
        #원본 복제
        self.dfCopyList = [ i.copy() for i in self.df_list]

        for df in self.dfCopyList:
            #컬럼 삭제 ['재무제표종류', '당기 1분기 3개월  '당기 1분기 누적', '전기 1분기 3개월', '전기 1분기 누적', '전기', '전전기']
            df.drop(columns=list(df.columns[0:1]) +list(df.columns[12:]), inplace=True) 

            #entity항목 수정 -> entity[기업코드]
            entity=df[df['항목코드'].str.contains('^entity')]['항목코드'].str.slice(0,14)
            df.loc[entity.index,['항목코드']] = entity
            
            #항목명 띄어쓰기 삭제
            df['항목명'] = df['항목명'].str.replace(' ', '')

            #재무재표 통합 : 상위파일에 없는 계정은 하위파일 계정으로 합산
            if len(self.mergeJamu) == 0:
                self.mergeJamu = df.copy()

            self.mergeJamu= pd.merge(self.mergeJamu,df, how='outer', on=list(df.columns), sort=True)

        print(self.mergeJamu)
        self.mergeJamu.to_csv('merge.csv', encoding='cp949')

if __name__ == '__main__':
    test = jamu()