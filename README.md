# Naver_Crowler

naver crowling 사용법

1) conda 환경에서 설치(자신이 설정한 anaconda 환경에서 설치)

   conda install -c conda-forge selenium

2) 크롬 드라이버 설치(네이버 크롤링을 하기 위해서는 크롬 드라이버 설치가 필수)

   brew install chromedriver

   ==> Auto-updating Homebrew...

   설치가 오래 걸릴 수 있으므로 기다리는 것을 추천

4) 크롬 드라이버 경로 확인

   which chromedriver

   /opt/homebrew/bin/chromedriver <- 이렇게 나오면 driver_path에 이 경로를 추가하면 됨.

5) naver_crawler.py 해당 경로 지정(driver_path = '/Users/yourname/tools/chromedriver')

6) naver_crawler.py 실행

      -> 자신이 찾고 싶은 빵은 메인 함수에서 지정해서 실행해야 함.
