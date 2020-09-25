from dotenv import load_dotenv
load_dotenv(verbose=True)

import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from flask_cors import CORS
from app.main import create_app, db, login_manager
from app.main.entities.report import Report
from app.main.entities.user import User, OAuth
from app.main.entities.emotionLexicon import EmotionLexicon
from app.main.entities.userStreamingTweets import UserStreamingTweets
from app.main.entities.tweetWithScores import TweetWithScores
from app.main.entities.tweetsTopic import TweetsTopic

app = create_app(os.getenv('ENV') or 'dev')

CORS(app, supports_credentials=True)

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    if(not os.getenv('ENV')):
        app.run(debug=os.getenv('FLASK_DEBUG'), host=os.getenv('HOST'),
                port=os.getenv('PORT'), use_reloader=False)
    else:
        app.run()


if __name__ == '__main__':
    manager.run()
