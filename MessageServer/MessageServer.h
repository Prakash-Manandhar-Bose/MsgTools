#ifndef MESSAGE_SERVER_H
#define MESSAGE_SERVER_H

#include <QObject>
#include <QPointer>
#include <QFile>
#include <QTextStream>
#include <QSettings>

#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QPlainTextEdit>

class QTcpServer;
class ServerPort;

#include "Message.h"

class MessageServer : public QMainWindow
{
    Q_OBJECT

    public:
        MessageServer(int argc, char *argv[]);

    private slots:
        void GotANewClient();
        void AddNewClient(ServerPort* serverPort);

        void LoadPlugin(QString fileName);
        void LoadPluginButton();

        void LogButton();
        void MessageSlot(QSharedPointer<Message> msg);

        void ClientDied();
    private:
        QPlainTextEdit*  _statusBox;
        QVBoxLayout* _layout;
        QPushButton* _logButton;
        QPushButton* _loadPluginButton;
        QSharedPointer<QFile> _logFile;
        QTcpServer* _tcpServer;
        QList<ServerPort*> _clients;
        QSettings _settings;
};

#endif