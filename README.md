# Odoo 15 дээр анхны CUSTOM MODULE
Анх удаа odoo 15 дээр туршилтын модуль хийж үзлээ.

**VSCode editor дээр odoo server ачааллах script**
```
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Odoo15",
      "type": "python",
      "request": "launch",
      "stopOnEntry": false,
      "python": "H:\\Odoo\\python\\python.exe",
      "console": "integratedTerminal",
      "program": "${workspaceRoot}/odoo-bin",
      "args": ["--config=H:\\Odoo\\server\\odoo.conf"],
      "cwd": "${workspaceRoot}",
      "env": {},
      "envFile": "${workspaceRoot}/.env",
      "debugOptions": ["RedirectOutput"]
    }
  ]
}
```
