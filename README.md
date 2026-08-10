# ⚡ Velox-Lang

Velox-Lang, Python ile sıfırdan yazılmış, basit ve öğretici amaçlı bir programlama dili yorumlayıcısıdır (interpreter). Kendi lexer, parser ve evaluator (AST tabanlı) katmanlarını içerir. Türkçe anahtar kelimeler kullanır ve etkileşimli bir REPL (canlı terminal) üzerinden çalışır.

Bu proje, bir programlama dilinin nasıl çalıştığını (tokenization → parsing → AST → evaluation) sıfırdan öğrenmek/anlamak isteyenler için hazırlanmıştır.

## ✨ Özellikler

- 🔢 Sayılarla (integer) işlem yapma
- 🔤 String (metin) desteği ve `+` ile birleştirme
- 📦 Değişken tanımlama ve erişim (`deger`)
- 🖨️ Ekrana yazdırma (`yaz`)
- 🔀 Koşullu ifadeler (`eger` / `yoksa`)
- ➕ Aritmetik operatörler: `+ - * /`
- 🔍 Karşılaştırma operatörleri: `== != < >`
- 💬 Etkileşimli REPL (canlı terminal) arayüzü

## 📥 Kurulum

Projeyi çalıştırmak için sadece Python 3 gereklidir (harici bağımlılık yoktur).

```bash
git clone https://github.com/kullanici-adin/velox-lang.git
cd velox-lang
python3 main.py
```

## 🚀 Kullanım

Programı çalıştırdığınızda karşınıza `velox >` istemi (prompt) çıkar:

```
=============================================
 ⚡ VELOX-LANG v1.2 (String & Metin Destekli) ⚡
 Çıkmak için 'cikis' yazın.
=============================================
velox >
```

Çıkmak için `cikis` yazabilirsiniz.

### Değişken tanımlama

```
velox > deger x = 10
velox > yaz(x)
10
```

### String kullanımı ve birleştirme

```
velox > deger isim = "Dünya"
velox > yaz("Merhaba, " + isim)
Merhaba, Dünya
```

### Aritmetik işlemler

```
velox > yaz(5 + 3 * 2)
11
```

### Karşılaştırma işlemleri

```
velox > yaz(5 > 3)
1
velox > yaz(5 == 3)
0
```

### Koşullu ifadeler (`eger` / `yoksa`)

```
velox > eger (5 > 3) { yaz("büyük") } yoksa { yaz("küçük") }
büyük
```

## 🧠 Dil Sözdizimi (Syntax) Özeti

| Anahtar Kelime / Operatör | Anlamı                    |
|----------------------------|----------------------------|
| `deger`                     | Değişken tanımlama         |
| `yaz(...)`                  | Ekrana yazdırma            |
| `eger (...) { ... }`        | If koşulu                  |
| `yoksa { ... }`             | Else bloğu                 |
| `+ - * /`                   | Aritmetik operatörler      |
| `== != < >`                 | Karşılaştırma operatörleri |
| `"..."`                     | String (metin) literal     |

## 🏗️ Proje Mimarisi

Yorumlayıcı klasik 4 katmandan oluşur:

1. **Lexer** – Kaynak kodu token'lara (jetonlara) ayırır (regex tabanlı).
2. **Parser** – Token dizisini bir AST (Soyut Sözdizimi Ağacı) yapısına dönüştürür.
3. **AST Düğümleri** – `NumberNode`, `StringNode`, `BinOpNode`, `VarAssignNode`, `IfNode` vb.
4. **Interpreter (Evaluator)** – AST'yi gezerek (visitor pattern) sonucu hesaplar/çalıştırır.

```
main.py
├── lexer()          # Kaynak kod -> Token listesi
├── Parser            # Token listesi -> AST
├── AST Node sınıfları
└── Interpreter        # AST -> Sonuç
```

## 🗺️ Yol Haritası (Fikirler)

- [ ] Döngüler (`iken`, `tekrar` vb.)
- [ ] Fonksiyon tanımlama desteği
- [ ] Listeler / diziler
- [ ] Yorum satırları (`//` veya `#`)
- [ ] Dosyadan kod çalıştırma (`.vlx` uzantılı dosyalar)
- [ ] Hata mesajlarında satır/sütun bilgisi

## 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Bir issue açabilir ya da doğrudan pull request gönderebilirsiniz.

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
