"""
spider関連のマッピングを定義する
"""

from enum import Enum

import scrapy

from scraper.spiders.techbiz import TechbizSpider


class Sites(str, Enum):
    """
    サイト名一覧
    """

    TECHBIZ = "techbiz"


# サイト名とspiderクラスのマッピング
SITE_SPIDER_MAPPING: dict[Sites, type[scrapy.Spider]] = {Sites.TECHBIZ: TechbizSpider}


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


# テックビズリクエスト時のスキル名とリクエストエンドポイント名のマッピング
TECHBIZ_TARGET_MAPPING: dict[TechbizMenuSkills, str] = {
    TechbizMenuSkills.JAVA: "skill-13",
    TechbizMenuSkills.PYTHON: "skill-4",
    TechbizMenuSkills.PHP: "skill-3",
    TechbizMenuSkills.AWS: "skill-57",
    TechbizMenuSkills.PMO: "skill-307",
    TechbizMenuSkills.PM: "skill-270",
    TechbizMenuSkills.RUBY: "skill-5",
    TechbizMenuSkills.GO: "skill-26",
    TechbizMenuSkills.SCALA: "skill-16",
    TechbizMenuSkills.TYPESCRIPT: "skill-2",
    TechbizMenuSkills.REACT: "skill-45",
    TechbizMenuSkills.VUEJS: "skill-41",
    TechbizMenuSkills.JAVASCRIPT: "skill-1",
    TechbizMenuSkills.NODEJS: "skill-84",
    TechbizMenuSkills.GCP: "skill-601",
    TechbizMenuSkills.AZURE: "skill-59",
    TechbizMenuSkills.PERL: "skill-6",
    TechbizMenuSkills.SWIFT: "skill-12",
    TechbizMenuSkills.KOTLIN: "skill-14",
    TechbizMenuSkills.UNITY: "skill-257",
    TechbizMenuSkills.C: "skill-9",
    TechbizMenuSkills.CSHARP: "skill-15",
    TechbizMenuSkills.CPLUSPLUS: "skill-10",
    TechbizMenuSkills.VBNET: "skill-38",
    TechbizMenuSkills.VB: "skill-30",
    TechbizMenuSkills.SQL: "skill-24",
    TechbizMenuSkills.R: "skill-27",
    TechbizMenuSkills.ANDROID: "skill-73",
    TechbizMenuSkills.IOS: "skill-72",
    TechbizMenuSkills.COBOL: "skill-22",
}
