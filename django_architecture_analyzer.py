import os
import django
import importlib
import inspect
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re


def setup_django():
    """Автоматичне налаштування Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education_platform_api.settings')
        django.setup()
        print("✅ Django успішно налаштовано")
        return True
    except Exception as e:
        print(f"❌ Помилка налаштування Django: {e}")
        return False


def discover_django_apps():
    """Знаходить всі додатки в проекті"""
    from django.apps import apps
    apps_list = []
    for app_config in apps.get_app_configs():
        if not app_config.name.startswith('django.'):
            apps_list.append(app_config)
    return apps_list


def analyze_app_structure(app_config):
    """Детально аналізує структуру додатка"""
    app_info = {
        'name': app_config.verbose_name,
        'models': [],
        'views': [],
        'urls': [],
        'templates': [],
        'admin': []
    }

    print(f"🔍 Аналізую додаток: {app_config.verbose_name}")

    # Моделі
    for model in app_config.get_models():
        fields = []
        for field in model._meta.fields[:6]:  # Перші 6 полів
            fields.append(f"{field.name} ({field.get_internal_type()})")

        app_info['models'].append({
            'name': model.__name__,
            'fields': fields,
            'field_count': len(model._meta.fields)
        })

    # Views
    try:
        views_module = importlib.import_module(f'{app_config.name}.views')
        for name, obj in inspect.getmembers(views_module):
            if (inspect.isfunction(obj) or inspect.isclass(obj)) and not name.startswith('_'):
                if any(keyword in name.lower() for keyword in ['view', 'page', 'list', 'detail', 'create', 'update']):
                    app_info['views'].append(name)
    except ImportError as e:
        print(f"   ⚠️ Не вдалося імпортувати views: {e}")

    # Templates
    templates_dirs = [
        Path('templates') / app_config.name,
        Path(app_config.path) / 'templates' / app_config.name
    ]

    for templates_dir in templates_dirs:
        if templates_dir.exists():
            for template_file in templates_dir.glob('*.html'):
                template_info = {
                    'name': template_file.name,
                    'path': str(template_file),
                    'components': analyze_template(template_file)
                }
                app_info['templates'].append(template_info)

    # Admin
    try:
        admin_module = importlib.import_module(f'{app_config.name}.admin')
        for name, obj in inspect.getmembers(admin_module):
            if hasattr(obj, 'model') and hasattr(obj, 'list_display'):
                app_info['admin'].append(name)
    except ImportError:
        pass

    return app_info


def analyze_template(template_path):
    """Аналізує шаблон та знаходить всі компоненти"""
    components = {
        'extends': None,
        'includes': [],
        'blocks': [],
        'static_files': [],
        'urls': []
    }

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # {% extends %}
            extends_match = re.search(r'\{%\s*extends\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
            if extends_match:
                components['extends'] = extends_match.group(1)

            # {% include %}
            includes = re.findall(r'\{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
            components['includes'] = includes

            # {% block %}
            blocks = re.findall(r'\{%\s*block\s+([^%}]+)\s*%\}', content)
            components['blocks'] = blocks

            # {% static %}
            static_files = re.findall(r'\{%\s*static\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
            components['static_files'] = static_files

            # {% url %}
            urls = re.findall(r'\{%\s*url\s+[\'"]([^\'"]+)[\'"]\s*%\}', content)
            components['urls'] = urls

    except Exception as e:
        print(f"   ⚠️ Помилка читання шаблону {template_path}: {e}")

    return components


def generate_clear_architecture_diagram(apps_data):
    """Генерує зрозумілу візуальну схему"""
    fig, ax = plt.subplots(figsize=(18, 14))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)

    # Кольори для різних типів компонентів
    colors = {
        'app': '#2E86AB',
        'model': '#A23B72',
        'view': '#F18F01',
        'template': '#C73E1D',
        'admin': '#3BB273'
    }

    y_start = 11
    app_height = 2.5

    for i, app_info in enumerate(apps_data):
        app_y = y_start - i * (app_height + 0.5)

        # Головний блок додатка
        app_rect = patches.FancyBboxPatch((1, app_y - app_height), 14, app_height,
                                          boxstyle="round,pad=0.1", linewidth=3,
                                          facecolor=colors['app'], alpha=0.9,
                                          edgecolor='#1A5276')
        ax.add_patch(app_rect)

        # Назва додатка
        ax.text(8, app_y - 0.3, app_info['name'],
                ha='center', va='center', fontsize=16, weight='bold', color='white')

        # Статистика додатка
        stats_text = f"Моделі: {len(app_info['models'])} | Views: {len(app_info['views'])} | Шаблони: {len(app_info['templates'])}"
        ax.text(8, app_y - 0.8, stats_text,
                ha='center', va='center', fontsize=11, color='white', style='italic')

        # Детальна інформація по компонентах
        detail_y = app_y - 1.5
        col_width = 3.5

        # Моделі
        if app_info['models']:
            models_text = "📊 Моделі:\n" + "\n".join([f"• {m['name']} ({m['field_count']} полів)"
                                                     for m in app_info['models'][:3]])
            if len(app_info['models']) > 3:
                models_text += f"\n• ... (+{len(app_info['models']) - 3})"

            ax.text(2.5, detail_y, models_text,
                    ha='left', va='top', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['model'], alpha=0.8))

        # Views
        if app_info['views']:
            views_text = "🎯 Views:\n" + "\n".join([f"• {v}" for v in app_info['views'][:4]])
            if len(app_info['views']) > 4:
                views_text += f"\n• ... (+{len(app_info['views']) - 4})"

            ax.text(6.5, detail_y, views_text,
                    ha='left', va='top', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['view'], alpha=0.8))

        # Шаблони
        if app_info['templates']:
            templates_text = "📄 Шаблони:\n" + "\n".join([f"• {t['name']}"
                                                         for t in app_info['templates'][:3]])
            if len(app_info['templates']) > 3:
                templates_text += f"\n• ... (+{len(app_info['templates']) - 3})"

            ax.text(10.5, detail_y, templates_text,
                    ha='left', va='top', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['template'], alpha=0.8))

    # Легенда
    legend_y = 0.5
    legend_items = [
        ("📊 Моделі", colors['model']),
        ("🎯 Views", colors['view']),
        ("📄 Шаблони", colors['template']),
        ("⚙️ Admin", colors['admin'])
    ]

    for i, (text, color) in enumerate(legend_items):
        ax.add_patch(patches.FancyBboxPatch((1 + i * 3.5, legend_y), 3, 0.3,
                                            boxstyle="round,pad=0.1",
                                            facecolor=color, alpha=0.8))
        ax.text(2.5 + i * 3.5, legend_y + 0.15, text,
                ha='center', va='center', fontsize=9, weight='bold')

    ax.set_aspect('equal')
    ax.axis('off')
    plt.title('🎯 Детальна архітектура Django проекту\n',
              fontsize=20, pad=30, weight='bold', color='#2C3E50')
    plt.tight_layout()
    plt.savefig('django_detailed_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='#F8F9FA', edgecolor='none')
    plt.close()


def generate_detailed_report(apps_data):
    """Генерує дуже детальний текстовий звіт"""
    with open('django_detailed_report.md', 'w', encoding='utf-8') as f:
        f.write("# 🎯 Детальний звіт архітектури Django проекту\n\n")

        for app_info in apps_data:
            f.write(f"## 📦 Додаток: {app_info['name']}\n\n")

            # Моделі
            if app_info['models']:
                f.write("### 📊 Моделі бази даних:\n")
                for model in app_info['models']:
                    f.write(f"#### {model['name']}\n")
                    f.write(f"- **Кількість полів:** {model['field_count']}\n")
                    if model['fields']:
                        f.write("- **Основні поля:**\n")
                        for field in model['fields']:
                            f.write(f"  - `{field}`\n")
                    f.write("\n")

            # Views
            if app_info['views']:
                f.write("### 🎯 Views (Контролери):\n")
                for view in app_info['views']:
                    f.write(f"- `{view}`\n")
                f.write("\n")

            # Шаблони
            if app_info['templates']:
                f.write("### 📄 Шаблони:\n")
                for template in app_info['templates']:
                    f.write(f"#### {template['name']}\n")
                    if template['components']['extends']:
                        f.write(f"- **Наслідує:** `{template['components']['extends']}`\n")
                    if template['components']['includes']:
                        f.write("- **Включає компоненти:**\n")
                        for inc in template['components']['includes']:
                            f.write(f"  - `{inc}`\n")
                    if template['components']['blocks']:
                        f.write("- **Блоки:**\n")
                        for block in template['components']['blocks']:
                            f.write(f"  - `{block}`\n")
                    f.write("\n")

            f.write("---\n\n")

        # Загальна статистика
        total_models = sum(len(app['models']) for app in apps_data)
        total_views = sum(len(app['views']) for app in apps_data)
        total_templates = sum(len(app['templates']) for app in apps_data)

        f.write("## 📈 Загальна статистика проекту\n\n")
        f.write(f"- **Кількість додатків:** {len(apps_data)}\n")
        f.write(f"- **Загальна кількість моделей:** {total_models}\n")
        f.write(f"- **Загальна кількість views:** {total_views}\n")
        f.write(f"- **Загальна кількість шаблонів:** {total_templates}\n")


def print_console_summary(apps_data):
    """Виводить зведення в консоль"""
    print("\n" + "=" * 60)
    print("🎯 ЗВЕДЕННЯ АРХІТЕКТУРИ ПРОЕКТУ")
    print("=" * 60)

    for app_info in apps_data:
        print(f"\n📦 ДОДАТОК: {app_info['name']}")
        print(f"   📊 Моделі: {len(app_info['models'])}")
        if app_info['models']:
            for model in app_info['models'][:3]:
                print(f"      • {model['name']} ({model['field_count']} полів)")
            if len(app_info['models']) > 3:
                print(f"      • ... (+{len(app_info['models']) - 3})")

        print(f"   🎯 Views: {len(app_info['views'])}")
        if app_info['views']:
            for view in app_info['views'][:3]:
                print(f"      • {view}")
            if len(app_info['views']) > 3:
                print(f"      • ... (+{len(app_info['views']) - 3})")

        print(f"   📄 Шаблони: {len(app_info['templates'])}")
        if app_info['templates']:
            for template in app_info['templates'][:2]:
                print(f"      • {template['name']}")
            if len(app_info['templates']) > 2:
                print(f"      • ... (+{len(app_info['templates']) - 2})")


def main():
    """Головна функція"""
    print("🚀 ЗАПУСК ДЕТАЛЬНОГО АНАЛІЗУ DJANGO ПРОЄКТУ...")
    print("=" * 50)

    if not setup_django():
        return

    # Знаходимо всі додатки
    apps = discover_django_apps()
    print(f"📦 Знайдено додатків: {len(apps)}")

    # Аналізуємо кожен додаток
    apps_data = []
    for app in apps:
        app_info = analyze_app_structure(app)
        apps_data.append(app_info)

    # Генеруємо результати
    print("\n🎨 СТВОРЕННЯ ВІЗУАЛІЗАЦІЇ...")
    generate_clear_architecture_diagram(apps_data)

    print("📊 СТВОРЕННЯ ДЕТАЛЬНОГО ЗВІТУ...")
    generate_detailed_report(apps_data)

    print("📋 ВИВЕДЕННЯ ЗВЕДЕННЯ...")
    print_console_summary(apps_data)

    print("\n" + "=" * 50)
    print("✅ АНАЛІЗ ЗАВЕРШЕНО!")
    print("📁 РЕЗУЛЬТАТИ:")
    print("   - 📊 django_detailed_architecture.png (Візуальна схема)")
    print("   - 📄 django_detailed_report.md (Детальний звіт)")
    print("   - 📋 Зведення вище (Консольна версія)")
    print("=" * 50)


if __name__ == "__main__":
    main()