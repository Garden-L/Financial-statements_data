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
        
        modify =pd.DataFrame()

        for df in self.dfCopyList:
            modify = pd.concat([modify,df[['항목코드','항목명']]], axis=0)
        
        modify = modify[~modify['항목코드'].str.contains(r'^(entity)')]
        modify.drop_duplicates('항목명', inplace=True)
        modify.set_index('항목명')

        i = 0
        for df in self.dfCopyList:
            #컬럼 삭제 ['재무제표종류', '당기 1분기 3개월  '당기 1분기 누적', '전기 1분기 3개월', '전기 1분기 누적', '전기', '전전기']
            df.drop(columns=list(df.columns[0:1]) +list(df.columns[13:]), inplace=True) 
            
            #항목명 띄어쓰기 삭제
            # df['항목명'] = df['항목명'].str.replace(' ', '')

            #형변환 (문자형)
            df=df.astype(str)
            #entity항목 수정 -> entity[기업코드]
            entity=df.loc[df['항목코드'].str.contains('^entity'),'항목코드'].str.slice(0,14)
            df.loc[entity.index,['항목코드']] = entity

            #entity
            tempIndex = df[df['항목코드'].str.contains(r'^(entity)')]

            tempIndex.set_index('항목명', inplace=True)
            tempIndex.update(modify['항목코드'])
            tempIndex.reset_index(inplace=True)
            
            df = df[['종목코드', '회사명', '시장구분', '업종', '업종명', '결산월', '결산기준일', '보고서종류', '통화', '항목코드', '항목명', '당기 1분기 3개월']]
            #재무재표 통합 : 상위파일에 없는 계정은 하위파일 계정으로 합산
            if len(self.mergeJamu) == 0:
                self.mergeJamu = df.copy()
            else:
                self.mergeJamu = pd.merge(self.mergeJamu,df, how='outer', on=list(df.columns[0:-1]), sort=True,suffixes=(f'_0', f'_1'))

                find = self.mergeJamu['당기 1분기 3개월_1'].isna()
                self.mergeJamu.loc[find,'당기 1분기 3개월_1'] = self.mergeJamu.loc[find,'당기 1분기 3개월_0'] 
                self.mergeJamu.drop(columns='당기 1분기 3개월_0', inplace=True)
                self.mergeJamu.rename(columns={'당기 1분기 3개월_1' : '당기 1분기 3개월'}, inplace=True)

            
                # print(len(set(self.mergeJamu['종목코드'])))
        # print(self.mergeJamu.columns[-4:])
        # for col in self.mergeJamu.columns[-5:]:
        #     print(col)
        #     print(self.mergeJamu[col].isna())
        # #금액설정
        # self.mergeJamu['당기 1분기 3개월'] = float('NaN')
        # print(reversed(self.df_list))
        # for df in reversed(self.df_list):
        #     self.mergeJamu = self.mergeJamu.combine_first(df)
        
        self.mergeJamu.to_csv('merge.csv', encoding='cp949')


if __name__ == '__main__':
    test = jamu()