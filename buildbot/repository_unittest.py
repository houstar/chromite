#!/usr/bin/python

# Copyright (c) 2011 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import functools
import mox
import sys
import unittest

import constants
sys.path.insert(0, constants.SOURCE_ROOT)
from chromite.buildbot import repository
from chromite.lib import cros_build_lib as cros_lib

# pylint: disable=W0212,R0904,E1101,W0613
class RepositoryTests(mox.MoxTestBase):

  def RunCommand_Mock(self, result, *args, **kwargs):
    output = self.mox.CreateMockAnything()
    output.output = result
    return output

  def testExternalRepoCheckout(self):
    """Test we detect external checkouts properly."""
    self.mox.StubOutWithMock(cros_lib, 'RunCommand')
    tests = [
        'http//git.chromium.org/chromiumos/manifest.git',
        'ssh://gerrit-int.chromium.org:29419/chromeos/manifest.git',
        'test@abcdef.bla.com:39291/bla/manifest.git',
        'test@abcdef.bla.com:39291/bla/manifest',
        'test@abcdef.bla.com:39291/bla/Manifest-internal',
     ]

    for test in tests:
      cros_lib.RunCommand = functools.partial(self.RunCommand_Mock, test)
      self.assertFalse(repository.IsInternalRepoCheckout('.'))

  def testInternalRepoCheckout(self):
    """Test we detect internal checkouts properly."""
    self.mox.StubOutWithMock(cros_lib, 'RunCommand')
    tests = [
        'ssh://gerrit-int.chromium.org:29419/chromeos/manifest-internal.git',
        'ssh://gerrit-int.chromium.org:29419/chromeos/manifest-internal',
        'ssh://gerrit.chromium.org:29418/chromeos/manifest-internal',
        'test@abcdef.bla.com:39291/bla/manifest-internal.git',
    ]

    for test in tests:
      cros_lib.RunCommand = functools.partial(self.RunCommand_Mock, test)
      self.assertTrue(repository.IsInternalRepoCheckout('.'))


if __name__ == '__main__':
  unittest.main()
