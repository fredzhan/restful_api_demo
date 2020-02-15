from flask import g

class CommentsModel:
    def __init__(self):
        pass

    def searchComments(self, keyword):
        QUERY_SQL = '''
            SELECT * FROM comments WHERE content LIKE '%{kw}%';
        '''
        records = g.db.query(QUERY_SQL.format(kw=keyword)).fetchall()
        result = {'data':[]}
        for r in records:
            r_dict = {}
            r_dict['id'], r_dict['content'], r_dict['creation_time'], r_dict['score'], r_dict['nickname'] =  r
            result['data'].append(r_dict)
        return result
