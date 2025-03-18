"""
スクレイパーで使用する型定義および設定値の構造を定義する。
"""

from enum import Enum


class TechbizMenuSkills(str, Enum):
    """
    テックビズの案件検索画面スキルメニュー一覧
    """

    JAVA = "Java"
    PYTHON = "Python"
    PHP = "PHP"
    AWS = "AWS"
    PMO = "PMO"
    PM = "PM"
    RUBY = "Ruby"
    GO = "Go"
    SCALA = "Scala"
    TYPESCRIPT = "TypeScript"
    REACT = "React"
    VUEJS = "Vue.js"
    JAVASCRIPT = "JavaScript"
    NODEJS = "Node.js"
    GCP = "Gcp"
    AZURE = "Azure"
    PERL = "Perl"
    SWIFT = "Swift"
    KOTLIN = "Kotlin"
    UNITY = "Unity"
    C = "C"
    CSHARP = "C#"
    CPLUSPLUS = "C++"
    VBNET = "VB.NET"
    VB = "VB"
    SQL = "SQL"
    R = "R"
    ANDROID = "Android"
    IOS = "iOS"
    COBOL = "COBOL"
