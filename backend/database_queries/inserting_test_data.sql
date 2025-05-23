insert into website_information (website_name, website_address, google_map, website_phone_number, website_email, website_facebook, website_linkedin, website_instagram) values
('LinguaBoost', 'Львів, вулиця Університетська, 1', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2573.1188728141615!2d24.01730289323558!3d49.840223897950956!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x473add717532da69%3A0xf0cb97b8441ff1fe!2z0LLRg9C70LjRhtGPINCj0L3RltCy0LXRgNGB0LjRgtC10YLRgdGM0LrQsCwgMSwg0JvRjNCy0ZbQsiwg0JvRjNCy0ZbQstGB0YzQutCwINC-0LHQu9Cw0YHRgtGMLCA3OTAwMA!5e0!3m2!1suk!2sua!4v1711193981060!5m2!1suk!2sua', '+38 (032) 239-43-25', 'zag_kan@lnu.edu.ua', 'https://www.facebook.com/franko.lviv.ua/?locale=uk_UA', 'https://ua.linkedin.com/school/national-university-%27ivan-franko%27%E2%80%8B-lviv/', 'https://www.instagram.com/lviv_university/');

insert into courses (creator_id, creation_date, course_name, course_image, difficult_level, course_description) values
('4', '2024-07-14', 'English Express', 'images/course_images/course_1_image.jpg', '★★★', 'Курс "English Express" допоможе вам відчувати себе впевнено в подорожах та міжкультурних комунікаціях. Ви навчитеся основним фразам і виразам для різних ситуацій: бронювання готелів, замовлення їжі, оренда транспорту та спілкування з місцевими. Окрім цього, ми вивчимо культурні особливості англомовних країн, що допоможе уникнути непорозумінь та зробить вашу подорож більш комфортною. Курс підходить для початківців та тих, хто хоче покращити свої навички спілкування під час поїздок за кордон.'),
('4', '2025-02-05', 'English for Everyday', 'images/course_images/course_2_image.jpg', '★★', 'Курс "English for Everyday" — це інтенсивна програма для тих, хто прагне швидко освоїти англійську мову. Ми зосередимося на практичних навичках спілкування, граматиці та лексичному запасі, використовуючи сучасні методики навчання. Заняття включають інтерактивні вправи, відео та аудіо матеріали, що допомагають легко сприймати мову. За 6 місяців ви досягнете впевненості у спілкуванні, покращите вимову та граматику, а також будете готові до реальних мовних ситуацій. Підходить для учнів середнього та просунутого рівня.'),
('5', '2025-04-19', 'English for Life', 'images/course_images/course_3_image.jpg', '★', 'Курс "English for Life" допоможе вам впевнено спілкуватися англійською в будь-яких ситуаціях. Ви розвинете навички говоріння, слухання, читання та письма через інтерактивні уроки, реальні діалоги та практичні вправи. Підходить для всіх рівнів — від початківців до просунутих. Заняття з досвідченими викладачами дозволять вам швидко подолати мовні бар''єри, покращити граматику та поповнити словниковий запас. Долучайтеся до курсу та відкривайте нові можливості для кар''єри, подорожей і особистого розвитку!');

insert into lessons (course_id, lesson_name) values
('1', 'Заняття 1'),
('1', 'Заняття 2'),
('1', 'Заняття 3'),
('2', 'Заняття 1'),
('3', 'Заняття 1');

insert into one_many_tasks (lesson_id, text, correct_answer, first_wrong_answer, second_wrong_answer, third_wrong_answer) values
('1', 'She && to the store every Saturday', 'goes', 'go', 'gone', 'going'),
('1', 'I && be back!', 'will', 'an', 'was', 'were'),
('2', 'London is && capital of Great Britain.', 'the', 'a', 'an', 'on'),
('2', 'They && to London last summer', 'traveled', 'travels', 'travel', 'traveling'),
('3', 'I && my keys at home this morning', 'left', 'leave', 'leaves', 'leaving'),
('3', 'We && dinner at 7 p.m. every evening', 'have', 'has', 'having', 'had'),
('3', 'He && a new book right now.', 'is reading', 'reads', 'read', 'reading'),
('4', 'I && to the gym three times a week.', 'go', 'goes', 'gone', 'going'),
('4', 'They && a new house next year.', 'will buy', 'buys', 'bought', 'buy'),
('4', 'She && a book at the moment.', 'is reading', 'read', 'reads', 'reading');

insert into fix_sentence_tasks (lesson_id, correct_text, bad_text) values
('1', 'Martha is at the grocery store, getting ready for a house party. She has a list of what she needs with her as she goes along.', 'Martha are at the grocery magazine, getting ready for a horse party. She has a list of what she needs with his as she going along.'),
('2', 'When exploring New York City, there are several different options for activities during a day trip. Some visitors come to see a show, visit art museums, or simply to shop in many of the city’s high-end retailers.', 'When exploring New York City, there are several different options for activities during an day tripping. Some visitors come to see the show, visit art museums, or simply to shop on many of the city’s high-end retailers.'),
('3', 'Valentine"s Day (or Saint Valentine"s Day) is a holiday that, in the United States, takes place on February 14, and technically signifies the accomplishments of St. Valentine, a third-century Roman saint.', 'Valentine"s Day (or Saint Valentine"s Day) is an holiday that, on the United States, takes place on February 14, and technically signifies to accomplishments the St. Valentine, a third-century Roman saint');

insert into translate_word_tasks (lesson_id, english_word, ukrainian_word) values
('1', 'Tree', 'Дерево'),
('2', 'River', 'Річка'),
('3', 'Spoon', 'Ложка'),
('4', 'Sky', 'Небо'),
('4', 'Flashlight', 'Ліхтарик');

insert into sequence_tasks (lesson_id, sequence_text) values
('1', 'The sun is shining brightly. It’s a beautiful day to go outside and enjoy the fresh air with friends.'),
('2', 'I like reading books in the evening. It helps me relax and escape into a different world full of adventures.'),
('3', 'My cat loves to play with toys. She runs around the house and enjoys chasing her favorite ball every morning.'),
('4', 'We went to the park yesterday. The weather was perfect, and we had a great time walking and talking.');

insert into accordance_tasks (lesson_id) values
('1'),
('2'),
('3'),
('4');

insert into accordance_task_variants (accordance_task_id, first_variant, second_variant) values
('1', 'Cat', 'A small, furry animal that likes to purr.'),
('1', 'Apple', 'A fruit that can be red, green, or yellow.'),
('1', 'Chair', 'A piece of furniture you sit on.'),
('1', 'Toast', 'A type of food that is often eaten for breakfast.'),
('2', 'What is your name?', 'My name is John.'),
('2', 'Where do you live?', 'I live in New York.'),
('2', 'What time is it?', 'It’s 3 PM.'),
('3', 'Good morning', 'Добрий ранок'),
('3', 'How are you?', 'Як ти?'),
('3', 'Good evening', 'Доброго вечора'),
('3', 'Thank you', 'Дякую'),
('4', 'Banana', 'Банан'),
('4', 'Sky', 'Небо'),
('4', 'Grass', 'Трава'),
('4', 'Ocean', 'Океан'),
('4', 'Shark', 'Акула');

insert into discussion_exercises (lesson_id, image, first_question, second_question, third_question, fourth_question) values
('1', 'images/exercise_images/chips.png', 'In your opinion, are chips a satisfying snack choice, or do they leave you feeling hungry shortly after eating them?', 'Chips are often seen as a quick, convenient snack, but do you think they are a good choice for health-conscious consumers?', 'What alternatives could companies offer to make chips healthier without compromising on taste?', 'How does the act of sharing a bag of chips in a social setting impact the overall experience of snacking?'),
('2', 'images/exercise_images/mushrooms.jpg', 'How do different types of mushrooms impact the flavor and texture of a dish, and do you think some varieties are underrated or overlooked in cooking?', 'Mushrooms are often considered a healthy food option, but do you think they are as nutritious as other vegetables?', 'Mushrooms are used in various cultures around the world, but some can be toxic if not prepared properly. How do you feel about the risks of foraging for mushrooms versus buying them from a store?', 'Do you think the trend of plant-based eating has led to a rise in the popularity of mushrooms as a meat substitute?'),
('4', 'images/exercise_images/tesla.jpg', 'Do you think electric cars are truly a sustainable solution to the environmental problems caused by traditional gasoline-powered vehicles, or are there other factors we should consider, like battery production and disposal?', 'Electric cars are often seen as a cleaner option, but do you think they are accessible enough to become mainstream? What are some barriers that might prevent more people from switching to electric vehicles?', 'How do you feel about the growing number of electric car charging stations in urban areas? Do you think the infrastructure is evolving fast enough to support the increasing demand for electric vehicles?', 'With the rise of electric vehicles, what do you think the future of traditional car brands will look like? Do you believe they can successfully transition to producing electric cars, or will new companies dominate the market?');

insert into reading_exercises (lesson_id, image, text) values
('1', 'images/exercise_images/frankfurt.jpg', 'Frankfurt is a vibrant city located in central Germany, known as a financial hub and a cultural center. It is home to the European Central Bank and the Frankfurt Stock Exchange, making it one of the world’s key financial capitals. The city blends modern skyscrapers with historic buildings, offering a unique contrast between its cutting-edge business district and traditional architecture. One of Frankfurt’s most famous landmarks is the Römer, a medieval town hall dating back to the 14th century. The city is also known for its museums, particularly along the Museum Embankment, which houses the Städel Museum and the German Film Museum. Frankfurt’s culinary scene is notable for its local dish, Handkäse mit Musik, a sour milk cheese served with onions. With a rich cultural life, excellent transport connections, and a growing tech scene, Frankfurt is not only a financial powerhouse but also a city that embraces innovation and history.'),
('2', 'images/exercise_images/global_warming.jpg', 'Global warming refers to the long-term increase in Earth average surface temperature due to human activities, particularly the burning of fossil fuels such as coal, oil, and natural gas. This process releases greenhouse gases like carbon dioxide, methane, and nitrous oxide into the atmosphere, which trap heat and cause the planet to warm. The effects of global warming are widespread and concerning. Rising temperatures contribute to melting polar ice caps, leading to rising sea levels, which threaten coastal cities and ecosystems. Extreme weather events such as heatwaves, droughts, and intense storms are becoming more frequent and severe. These changes also affect agriculture, biodiversity, and human health, leading to food shortages, habitat loss, and increased disease. To combat global warming, governments, organizations, and individuals are focused on reducing emissions, transitioning to renewable energy sources, and promoting sustainable practices to mitigate the damage and prevent further temperature rise.'),
('3', 'images/exercise_images/ai.jpg', 'Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, learn, and problem-solve. AI systems are designed to analyze data, recognize patterns, and make decisions with minimal human intervention. These technologies can be categorized into two types: narrow AI, which is designed for specific tasks (like voice assistants or recommendation systems), and general AI, which would have the ability to perform any intellectual task that a human can do (though it’s still theoretical at this point). AI has a profound impact on various industries. In healthcare, it helps with diagnosing diseases and developing personalized treatment plans. In business, AI is used for automating processes, improving customer service, and analyzing large datasets. AI also plays a key role in autonomous vehicles, finance, and entertainment. However, as AI technology advances, concerns about ethics, job displacement, and privacy arise. Balancing innovation with responsible usage is critical to ensure AI benefits society as a whole.');

insert into listening_exercises (lesson_id, name, audio, text) values
('1', 'Canada', 'audio/canada.mp3', 'Canada is the second-largest country in the world, located in North America, known for its vast landscapes, multicultural society, and high quality of life. It has ten provinces and three territories, with cities like Toronto, Vancouver, and Montreal being cultural and economic hubs. Canada boasts diverse natural beauty, from the Rocky Mountains to pristine lakes and expansive forests. It is famous for its maple syrup, hockey, and bilingualism, with both English and French as official languages. With a strong economy, universal healthcare, and a reputation for politeness, Canada is often considered one of the best places to live.'),
('2', 'Fried fries', 'audio/fried_fries.mp3', 'Fried fries, also known as French fries, are a popular snack or side dish made from potatoes. The potatoes are typically cut into long, thin strips and deep-fried in oil until crispy and golden brown. They can be served in various forms, such as shoestring, thick-cut, or waffle fries, and are often seasoned with salt. Fried fries are commonly enjoyed with condiments like ketchup, mayonnaise, or vinegar, and are a staple in fast food restaurants and casual dining. Originally from Belgium or France, fried fries have become a beloved comfort food worldwide, with endless variations depending on region and taste preferences.'),
('3', 'Belgium chocolate', 'audio/belgium_chocolate.mp3', 'Belgium chocolate is renowned worldwide for its exceptional quality and craftsmanship. Made from high-quality cocoa beans, Belgian chocolate is known for its smooth texture, rich flavor, and careful production methods. Belgium has a long history of chocolate-making, with traditions dating back to the 17th century. The country is home to many famous chocolatiers, such as Godiva, Neuhaus, and Léonidas, who are known for their pralines, truffles, and other chocolate delights. Belgian chocolate is often crafted using traditional techniques, such as tempering, which ensures a glossy finish and smooth consistency. The chocolate is typically made with a high cocoa content, giving it a deep, indulgent flavor. It is considered one of the finest chocolates in the world and is often enjoyed as a luxurious treat or given as gifts.'),
('4', 'Buddhism', 'audio/buddhism.mp3', 'Buddhism is a spiritual and philosophical tradition founded by Siddhartha Gautama, known as the Buddha, in the 5th to 4th century BCE in India. It emphasizes the path to enlightenment through practices such as meditation, ethical living, and wisdom. The core teachings of Buddhism are encapsulated in the Four Noble Truths, which address the nature of suffering and the way to overcome it, and the Eightfold Path, which outlines the practical steps to live a moral, mindful, and focused life. Buddhism teaches that suffering arises from desire and attachment, and liberation (nirvana) is achieved by overcoming these through ethical conduct, meditation, and wisdom. There are various schools of Buddhism, including Theravada, Mahayana, and Vajrayana, each with unique practices and interpretations of the Buddha teachings. Today, Buddhism is practiced by millions worldwide and has influenced many aspects of culture, philosophy, and psychology.');

insert into vocabulary_exercises (lesson_id) values
('1'),
('2'),
('3');

insert into vocabulary_words (vocabulary_exercise_id, english_word, ukrainian_word, transcription) values
('1', 'Apple', 'Яблуко', 'ˈæpəl'),
('1', 'Water', 'Вода', 'ˈwɔːtər'),
('1', 'Tree', 'Дерево', 'triː'),
('1', 'Sun', 'Сонце', 'sʌn'),
('2', 'House', 'Будинок', 'haʊs'),
('2', 'Table', 'Стіл', 'ˈteɪbəl'),
('2', 'Chair', 'Крісло', 'ʧɛr'),
('3', 'Friend', 'Друг', 'frɛnd'),
('3', 'Happy', 'Щасливий', 'ˈhæpi');

insert into rules_exercises (lesson_id, image, text) values
('1', 'images/exercise_images/past_simple_tense_rules.jpg', 'Past Simple використовується для опису завершених дій у минулому. Зазвичай вживається з часоими виразами, такими як yesterday, last week, in 1990 тощо. Формула: особа + дієслово в минулому. Наприклад: "I played football yesterday." Заперечення утворюється за допомогою "did not" + основна форма дієслова: "I did not go to the party."'),
('2', 'images/exercise_images/present_simple_tense_rules.jpg', 'Present Simple використовується для вираження регулярних дій, загальних істин або фактів. Формула: особа + основна форма дієслова (для he/she додавання -s). Наприклад: "She reads books every day." Заперечення утворюється через "do not" або "does not": "They do not like coffee."'),
('3', 'images/exercise_images/future_perfect_tense_rules.jpg', 'Future Perfect описує дію, яка буде завершена до певного моменту в майбутньому. Формула: will have + past participle. Наприклад: "By next week, I will have finished the project." Цей час підкреслює завершення дії в майбутньому. Заперечення: "I will not have finished the work by then."');

insert into student_courses (student_id, course_id) values
('6', '1'),
('6', '2'),
('7', '1'),
('7', '2'),
('8', '1'),
('9', '2'),
('9', '3');

insert into student_applications (application_datetime, course_id, student_id, application_status) values
(NOW(), '1', '6', 'Підтверджено'),
(NOW(), '2', '6', 'Підтверджено'),
(NOW(), '1', '7', 'Підтверджено'),
(NOW(), '2', '7', 'Підтверджено'),
(NOW(), '1', '8', 'Підтверджено'),
(NOW(), '2', '9', 'Підтверджено'),
(NOW(), '3', '9', 'Підтверджено'),
(NOW(), '3', '6', 'В обробці'),
(NOW(), '3', '7', 'В обробці'),
(NOW(), '1', '9', 'Відхилено'),
(NOW(), '1', '9', 'В обробці');

insert into lesson_test_results (test_datetime, lesson_id, student_id, number_of_tests, test_result, is_successfully_passed) values
(NOW(), '1', '6', 6, 2, FALSE),
(NOW(), '1', '6', 6, 5, TRUE),
(NOW(), '2', '6', 6, 3, TRUE),
(NOW(), '3', '6', 7, 4, TRUE),
(NOW(), '1', '7', 6, 2, FALSE),
(NOW(), '2', '7', 6, 3, TRUE);

insert into course_final_test_results (test_datetime, course_id, student_id, number_of_tests, test_result, is_successfully_passed) values
(NOW(), '1', '6', 19, 10, TRUE);
