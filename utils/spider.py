#encoding:utf-8
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import json
from utils.db import Sqllite
from utils.env_vars import LOGGER, REQUESTS
import requests
from time import sleep, time

s = requests.session()

class Comment:
    def __init__(self, id, content, creation_time, score, nickname):
        self.id = id
        self.content = content
        self.creation_time = creation_time
        self.score = score
        self.nickname = nickname

    def __str__(self):
        return str(self.__dict__)

    def to_sql(self):
        r = "('{id}', '{content}', '{creation_time}', {score}, '{nickname}')" \
            .format(id = self.id, \
                    content=self.content,\
                    creation_time= self.creation_time, \
                    score = self.score,\
                    nickname = self.nickname
            )
        return r


class Spider:
    def __init__(self):
        LOGGER.info('Initiating Spider ...')
        (self.url, self.params, self.header) = REQUESTS
        self.db = Sqllite()
        CREATE_TABLE_SQL = '''
            CREATE TABLE IF NOT EXISTS comments (
                id              INT PRIMARY KEY     NOT NULL,
                content         TEXT                NOT NULL,
                creation_time   DATETIME            NOT NULL,
                score           INT,
                nickname        VARCHAR(50)
            );
        '''
        self.db.execute(CREATE_TABLE_SQL)
        self.session = requests.session()
        self.init_count = self.__count_records()
        self.task_id = int(time())
        LOGGER.info('Spider launched (task_id={id})'.format(id=self.task_id))



    def crawl(self, job_interval_in_sec=1):
        # TODO: threadPool
        for param in self.params:
            LOGGER.info('Requesting url:{url}, param:{param}, header:{header}'.format(url=self.url, param=param, header=self.header))
            t = self.session.get(self.url, params=param, headers=self.header).text
            data=json.loads(t[26:-2],strict=False)
            for c in data['comments']:
                id = c.get('id','')
                content = c.get('content','')
                creation_time = c.get('creationTime','')
                score = c.get('score','')
                nickname = c.get('nickname','')
                comment = Comment(id, content, creation_time, score, nickname)
                self.__load(comment)
            sleep(job_interval_in_sec)

        final_count = self.__count_records()
        LOGGER.info('{delta} new records loaded into DB. Latest total # of records: {total}'.format(delta=max(0, final_count-self.init_count), total=final_count))
        LOGGER.info('Spider(task_id={id}) completed.'.format(id=self.task_id))


    def __load(self, comment):
        LOAD_DATA_SQL = '''
            INSERT OR IGNORE INTO comments (id, content, creation_time, score, nickname)
            VALUES {record};
        '''
        self.db.execute(LOAD_DATA_SQL.format(record=comment.to_sql()))
        LOGGER.debug('Upserted:'+ comment.to_sql())

    def __count_records(self):
        COUNT_QUERY = '''
            SELECT COUNT(*) FROM comments;
        '''
        return self.db.query(COUNT_QUERY).fetchone()[0]

s = Spider()
s.crawl()

