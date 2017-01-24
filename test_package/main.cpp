#include <QApplication>
#include <QTextEdit>
#include <QFontDatabase>
int main(int argv, char **args)
{
   QApplication app(argv, args);
   QTextEdit textEdit;
   textEdit.show();

   QFontDatabase::addApplicationFont("./DejaVuSans.ttf");

  return app.exec();
}
