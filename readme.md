```
collecting... pkgs=['testing']
collected! len(tests)=3
testing.test_zap:test_spam ✅
testing.foo.test_bar:test_fail ❌
failed: test='testing.foo.test_bar:test_fail'
Traceback (most recent call last):
  File "pieskytest.py", line 46, in main
    fn()
  File "/home/graingert/projects/pieskytest/testing/foo/test_bar.py", line 6, in test_fail
    assert False
AssertionError
testing.foo.test_bar:test_ham ✅
```
